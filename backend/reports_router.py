"""
reports_router.py — FastAPI router for pothole report CRUD + clustering.

Mount into the main app:
    from reports_router import router as reports_router
    app.include_router(reports_router)
"""

import math
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Report, ReportCreate, ReportOut, StatusUpdate, ClusterOut, SeverityLevel, ReportStatus

router = APIRouter(tags=["Reports"])

# Severity ranking for "highest severity" comparisons
_SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2}


# ---------------------------------------------------------------------------
# Haversine helper
# ---------------------------------------------------------------------------

def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in **metres** between two points."""
    R = 6_371_000  # Earth radius in metres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_nearby_reports(
    lat: float,
    lon: float,
    db: Session,
    radius_m: float = 50.0,
) -> List[Report]:
    """Return all reports within `radius_m` metres of (lat, lon)."""
    all_reports = db.query(Report).all()
    return [
        r
        for r in all_reports
        if _haversine_m(lat, lon, r.lat, r.lon) <= radius_m
    ]


# ---------------------------------------------------------------------------
# CRUD endpoints
# ---------------------------------------------------------------------------

@router.get("/reports/clusters", response_model=List[ClusterOut])
def get_clusters(
    radius_m: float = Query(50.0, description="Cluster radius in metres"),
    db: Session = Depends(get_db),
):
    """
    Group all reports into spatial clusters using a greedy approach:
    iterate through reports and assign each to the first cluster whose
    centre is within `radius_m`, or start a new cluster.
    """
    reports = db.query(Report).order_by(Report.timestamp.desc()).all()
    clusters: list[dict] = []

    for r in reports:
        placed = False
        for c in clusters:
            if _haversine_m(c["center_lat"], c["center_lon"], r.lat, r.lon) <= radius_m:
                # Update running average of centre
                n = len(c["ids"])
                c["center_lat"] = (c["center_lat"] * n + r.lat) / (n + 1)
                c["center_lon"] = (c["center_lon"] * n + r.lon) / (n + 1)
                c["ids"].append(r.id)
                if _SEVERITY_RANK.get(r.severity, 0) > _SEVERITY_RANK.get(c["severity"], 0):
                    c["severity"] = r.severity
                placed = True
                break
        if not placed:
            clusters.append(
                {
                    "center_lat": r.lat,
                    "center_lon": r.lon,
                    "ids": [r.id],
                    "severity": r.severity,
                }
            )

    return [
        ClusterOut(
            center_lat=round(c["center_lat"], 6),
            center_lon=round(c["center_lon"], 6),
            report_count=len(c["ids"]),
            highest_severity=c["severity"],
            report_ids=c["ids"],
        )
        for c in clusters
    ]


@router.get("/reports", response_model=List[ReportOut])
def list_reports(
    status: Optional[ReportStatus] = Query(None, description="Filter by status: pending | fixed"),
    severity: Optional[SeverityLevel] = Query(None, description="Filter by severity: low | medium | high"),
    db: Session = Depends(get_db),
):
    """Return all reports, newest first.  Optionally filter by status and/or severity."""
    q = db.query(Report)
    if status:
        q = q.filter(Report.status == status)
    if severity:
        q = q.filter(Report.severity == severity)
    return q.order_by(Report.timestamp.desc()).all()


@router.get("/reports/{report_id}", response_model=ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Return a single report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/reports", response_model=ReportOut, status_code=201)
def create_report(body: ReportCreate, db: Session = Depends(get_db)):
    """
    Create a new pothole report.
    Called internally after the /detect endpoint finishes inference.
    """
    report = Report(**body.model_dump())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.patch("/reports/{report_id}", response_model=ReportOut)
def update_report_status(
    report_id: int,
    body: StatusUpdate,
    db: Session = Depends(get_db),
):
    """Mark a report as fixed (or revert to pending)."""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = body.status
    db.commit()
    db.refresh(report)
    return report

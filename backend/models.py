"""
models.py — SQLAlchemy ORM model + Pydantic schemas for pothole reports.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Literal

from sqlalchemy import Column, Integer, String, Float, DateTime
from pydantic import BaseModel, Field

from database import Base


# ---------------------------------------------------------------------------
# Enums (used for validation and Swagger docs)
# ---------------------------------------------------------------------------

class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ReportStatus(str, Enum):
    pending = "pending"
    fixed = "fixed"


# ---------------------------------------------------------------------------
# SQLAlchemy ORM model
# ---------------------------------------------------------------------------

class Report(Base):
    """A single pothole report tied to a geo-tagged image detection."""

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image_url = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    severity = Column(String, nullable=False)          # "low" | "medium" | "high"
    pothole_count = Column(Integer, nullable=False, default=1)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="pending")         # "pending" | "fixed"


# ---------------------------------------------------------------------------
# Pydantic schemas (request / response)
# ---------------------------------------------------------------------------

class ReportCreate(BaseModel):
    """Body for POST /reports."""
    image_url: str
    lat: float
    lon: float
    severity: SeverityLevel
    pothole_count: int = Field(..., ge=1)


class ReportOut(BaseModel):
    """Serialised report returned by GET endpoints."""
    id: int
    image_url: str
    lat: float
    lon: float
    severity: str
    pothole_count: int
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True          # allows ORM → Pydantic conversion


class StatusUpdate(BaseModel):
    """Body for PATCH /reports/{id}."""
    status: ReportStatus


class ClusterOut(BaseModel):
    """One cluster returned by GET /reports/clusters."""
    center_lat: float
    center_lon: float
    report_count: int
    highest_severity: str
    report_ids: List[int]

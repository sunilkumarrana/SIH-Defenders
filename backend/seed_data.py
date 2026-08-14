"""
seed_data.py — Insert 10 sample pothole reports for testing.

Run:  python seed_data.py
Some points are deliberately within 50 m of each other to exercise clustering.
"""

import random
from datetime import datetime, timedelta, timezone

from database import engine, SessionLocal, Base
from models import Report


def seed():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    
    # Clear existing records to ensure clean deterministic seeds
    db.query(Report).delete()
    db.commit()

    # Base coordinate — central Delhi (India Gate area)
    BASE_LAT = 28.6129
    BASE_LON = 77.2295

    # ~0.00022 degrees ≈ 25 m at this latitude
    CLOSE_OFFSET = 0.0002
    FAR_OFFSET = 0.005

    samples = [
        # ---- Cluster A (3 reports near India Gate) ----
        {
            "image_url": "https://example.com/images/pothole_a1.jpg",
            "lat": BASE_LAT,
            "lon": BASE_LON,
            "severity": "high",
            "pothole_count": 3,
            "status": "pending",
        },
        {
            "image_url": "https://example.com/images/pothole_a2.jpg",
            "lat": BASE_LAT + CLOSE_OFFSET,
            "lon": BASE_LON + CLOSE_OFFSET * 0.5,
            "severity": "medium",
            "pothole_count": 1,
            "status": "pending",
        },
        {
            "image_url": "https://example.com/images/pothole_a3.jpg",
            "lat": BASE_LAT - CLOSE_OFFSET * 0.3,
            "lon": BASE_LON + CLOSE_OFFSET,
            "severity": "low",
            "pothole_count": 1,
            "status": "fixed",
        },
        # ---- Cluster B (3 reports ≈ 500 m away) ----
        {
            "image_url": "https://example.com/images/pothole_b1.jpg",
            "lat": BASE_LAT + FAR_OFFSET,
            "lon": BASE_LON + FAR_OFFSET,
            "severity": "high",
            "pothole_count": 5,
            "status": "pending",
        },
        {
            "image_url": "https://example.com/images/pothole_b2.jpg",
            "lat": BASE_LAT + FAR_OFFSET + CLOSE_OFFSET,
            "lon": BASE_LON + FAR_OFFSET,
            "severity": "medium",
            "pothole_count": 2,
            "status": "pending",
        },
        {
            "image_url": "https://example.com/images/pothole_b3.jpg",
            "lat": BASE_LAT + FAR_OFFSET,
            "lon": BASE_LON + FAR_OFFSET + CLOSE_OFFSET,
            "severity": "high",
            "pothole_count": 4,
            "status": "fixed",
        },
        # ---- Cluster C (2 reports ≈ 1 km away) ----
        {
            "image_url": "https://example.com/images/pothole_c1.jpg",
            "lat": BASE_LAT - FAR_OFFSET * 2,
            "lon": BASE_LON - FAR_OFFSET,
            "severity": "low",
            "pothole_count": 1,
            "status": "pending",
        },
        {
            "image_url": "https://example.com/images/pothole_c2.jpg",
            "lat": BASE_LAT - FAR_OFFSET * 2 + CLOSE_OFFSET,
            "lon": BASE_LON - FAR_OFFSET,
            "severity": "medium",
            "pothole_count": 2,
            "status": "pending",
        },
        # ---- Isolated reports (no cluster) ----
        {
            "image_url": "https://example.com/images/pothole_d1.jpg",
            "lat": BASE_LAT + FAR_OFFSET * 3,
            "lon": BASE_LON - FAR_OFFSET * 2,
            "severity": "low",
            "pothole_count": 1,
            "status": "fixed",
        },
        {
            "image_url": "https://example.com/images/pothole_d2.jpg",
            "lat": BASE_LAT - FAR_OFFSET * 4,
            "lon": BASE_LON + FAR_OFFSET * 3,
            "severity": "high",
            "pothole_count": 6,
            "status": "pending",
        },
    ]

    now = datetime.now(timezone.utc)
    for i, s in enumerate(samples):
        s["timestamp"] = now - timedelta(hours=random.randint(1, 72))
        db.add(Report(**s))

    db.commit()
    print(f"[OK] Seeded {len(samples)} reports into the database.")
    db.close()


if __name__ == "__main__":
    seed()

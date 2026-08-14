"""
main.py — SIH-Defenders FastAPI entry point.

Starts the backend API server.  All report endpoints live in reports_router.py.
Run:  uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from reports_router import router as reports_router

# Create all tables on startup (hackathon-friendly, no migrations needed)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIH-Defenders Backend API",
    description="AI-Powered Pothole Detection & Reporting System",
    version="0.1.0",
)

# Allow frontend / dashboard to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the reports router
app.include_router(reports_router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "SIH-Defenders Backend API is running"}

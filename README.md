# SIH-Defenders: AI-Powered Pothole Detection & Reporting System

## Problem Statement
Road potholes and surface damages cause thousands of traffic accidents, severe vehicle damage, and significant road maintenance delays every year. Manual detection and reporting of road hazards is slow, inconsistent, and resource-intensive. 

**SIH-Defenders** is an end-to-end AI-powered automated pothole detection, assessment, and municipal reporting ecosystem. By combining real-time computer vision with geospatial reporting and a centralized administrative dashboard, the platform accelerates road repairs and improves citizen safety.

**Team Name**: Defenders

## Tech Stack
- **Backend**: FastAPI, Uvicorn, Python-Multipart, SQLAlchemy
- **Frontend**: React (Mobile reporting application with camera capture and geo-tagged submission)
- **Dashboard**: Web Dashboard (Map visualization using Leaflet.js / Google Maps API for municipal management)
- **ML Model**: YOLOv8 (Automated computer vision model for pothole detection and severity classification)
- **Docs**: Markdown API Specifications and Pitch Documentation

## Project Structure
```text
SIH-Defenders/
├── backend/
│   ├── main.py            # FastAPI entry point & health check
│   ├── requirements.txt   # Python dependencies
│   └── README.md
├── frontend/
│   └── README.md          # React client app
├── dashboard/
│   └── README.md          # Map dashboard for municipal authority
├── ml-model/
│   ├── inference.py       # Pothole detection inference stub
│   └── README.md          # YOLOv8 model instructions
├── docs/
│   ├── api-contract.md    # REST API endpoints & payload schemas
│   └── pitch-notes.md     # Research, impact metrics & demo script
├── .gitignore
└── README.md
```

## How to Run Locally

### 1. Backend Service
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API server will be available at `http://127.0.0.1:8000`.

### 2. Frontend Application
```bash
cd frontend
npm install
npm start
```

### 3. Dashboard Application
```bash
cd dashboard
npm install
npm start
```

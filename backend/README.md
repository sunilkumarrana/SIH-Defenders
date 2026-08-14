# Backend — Database & Reports Module

## Quick Start

```bash
cd backend
pip install -r requirements.txt

# Seed the database with 10 sample reports
python seed_data.py

# Start the server
uvicorn main:app --reload
```

The API docs will be at **http://127.0.0.1:8000/docs** (Swagger UI).

---

## For Teammates — Mounting This Router

If you're building the main FastAPI app (e.g., Sunil adding the `/detect` endpoint), just import and include the router:

```python
from fastapi import FastAPI
from reports_router import router as reports_router

app = FastAPI(title="SIH-Defenders Backend API")
app.include_router(reports_router)
```

After a detection completes, create a report by POSTing to `/reports`:

```python
import httpx

httpx.post("http://localhost:8000/reports", json={
    "image_url": "https://bucket.example.com/img123.jpg",
    "lat": 28.6129,
    "lon": 77.2295,
    "severity": "high",
    "pothole_count": 3,
})
```

---

## API Endpoints

| Method  | Path                  | Description                                  |
| ------- | --------------------- | -------------------------------------------- |
| GET     | `/reports`            | List all reports (filter: `?status=`, `?severity=`) |
| GET     | `/reports/{id}`       | Get a single report                          |
| POST    | `/reports`            | Create a new report                          |
| PATCH   | `/reports/{id}`       | Update report status (`{"status": "fixed"}`) |
| GET     | `/reports/clusters`   | Spatial clusters within 50 m radius          |

---

## File Structure

| File                | Purpose                                       |
| ------------------- | --------------------------------------------- |
| `database.py`       | SQLAlchemy engine, session factory, `get_db`  |
| `models.py`         | `Report` ORM model + Pydantic schemas         |
| `reports_router.py` | FastAPI router (CRUD + clustering)            |
| `seed_data.py`      | Insert 10 sample reports for testing          |
| `main.py`           | App entry point (mounts router, creates tables) |

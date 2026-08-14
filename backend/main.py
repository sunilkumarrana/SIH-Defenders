from fastapi import FastAPI

app = FastAPI(title="SIH-Defenders Backend API")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "SIH-Defenders Backend API is running"}

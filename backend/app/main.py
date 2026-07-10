from datetime import datetime, timezone

from fastapi import FastAPI


app = FastAPI(
    title="Task Tracker API",
    description="Module 1 Task Tracker REST API learning project",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
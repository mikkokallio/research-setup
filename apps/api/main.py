import os
from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI()

RUN_KEY = os.getenv("RUN_KEY", "local")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/info")
def info():
    return {
        "run_key": RUN_KEY,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "alpha": 0.123,
            "beta": 0.456,
            "series": [1, 2, 3, 4, 5],
        },
    }

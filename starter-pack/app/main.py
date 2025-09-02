
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import os

app = FastAPI(
    title="ULOS Consciousness Engine API",
    version="0.1.0",
    description="Contracts for ingest, artifacts, notes, embeddings, and market-listening outputs."
)

class Health(BaseModel):
    status: str
    postgres_url: str | None = None
    neo4j_url: str | None = None
    nats_url: str | None = None

def get_settings():
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "NEO4J_URL": os.getenv("NEO4J_URL"),
        "NATS_URL": os.getenv("NATS_URL"),
    }

@app.get("/health", response_model=Health, tags=["internal"])
def health(settings: dict = Depends(get_settings)):
    return Health(
        status="ok",
        postgres_url=settings["DATABASE_URL"],
        neo4j_url=settings["NEO4J_URL"],
        nats_url=settings["NATS_URL"],
    )

@app.get("/v1/findings/market", tags=["findings"])
def market_findings(sample: bool = True):
    """Temporary stub. Returns a sample payload shaped for the UI and reports."""
    sample_doc = {
        "source": "reddit",
        "thread_url": "https://www.reddit.com/r/example/thread/abc123",
        "title": "Pain point: vendor lock-in with XYZ tool",
        "signal": {"sentiment": -0.62, "intensity": 0.74, "tags": ["lock-in", "pricing", "support"]},
        "excerpts": [
            "We can't export data without paying an absurd fee.",
            "Support tickets sit for weeks."
        ]
    }
    return {"items": [sample_doc] if sample else []}

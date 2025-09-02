
from fastapi import FastAPI
from .routes import health, artifacts, notes, findings

app = FastAPI(
    title="ULOS Consciousness Engine API",
    version="0.1.0",
    description="Contracts for ingest, artifacts, notes, embeddings, and market-listening outputs."
)

# include routers
app.include_router(health.router, tags=["internal"])
app.include_router(artifacts.router, prefix="/v1/artifacts", tags=["artifacts"])
app.include_router(notes.router, prefix="/v1/notes", tags=["notes"])
app.include_router(findings.router, prefix="/v1/findings", tags=["findings"])

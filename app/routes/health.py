
from fastapi import APIRouter
import os
router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "database_url": os.getenv("DATABASE_URL"),
        "neo4j_url": os.getenv("NEO4J_URL"),
        "nats_url": os.getenv("NATS_URL"),
    }

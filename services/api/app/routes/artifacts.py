
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Artifact(BaseModel):
    id: str
    title: str
    url: str | None = None
    author: str | None = None

fake_db = []

@router.post("/", response_model=Artifact)
def create_artifact(artifact: Artifact):
    fake_db.append(artifact)
    return artifact

@router.get("/", response_model=List[Artifact])
def list_artifacts():
    return fake_db

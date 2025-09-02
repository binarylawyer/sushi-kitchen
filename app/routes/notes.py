
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Note(BaseModel):
    id: str
    artifact_id: str
    content: str
    llm: str | None = None

fake_notes: list[Note] = []

@router.post("/", response_model=Note)
def create_note(note: Note):
    fake_notes.append(note)
    return note

@router.get("/", response_model=List[Note])
def list_notes():
    return fake_notes

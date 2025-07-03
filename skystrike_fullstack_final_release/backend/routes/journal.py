from fastapi import APIRouter, Request

router = APIRouter()


from pydantic import BaseModel

class JournalEntry(BaseModel):
    timestamp: str
    note: str
    strategy: str

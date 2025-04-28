from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    body: str = Field(..., description="The content of the note")
    contact_id: int

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    body: Optional[str] = Field(None, description="The content of the note")
    contact_id: Optional[int] = None

class NoteInDB(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Note(NoteInDB):
    pass 
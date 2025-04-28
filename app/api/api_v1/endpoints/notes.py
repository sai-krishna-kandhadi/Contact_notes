from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.note import Note, NoteCreate, NoteUpdate
from app.services import note_service
from app.worker import process_note_creation

router = APIRouter()

@router.get("/", response_model=List[Note])
def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    notes = note_service.get_notes(db, skip=skip, limit=limit)
    return notes

@router.post("/", response_model=Note)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    # Normalize note body field
    if hasattr(note, 'note_text'):
        note.body = note.note_text
    elif hasattr(note, 'note_body'):
        note.body = note.note_body
    
    db_note = note_service.create_note(db=db, note=note)
    
    # Trigger async processing
    process_note_creation.delay(db_note.id)
    
    return db_note

@router.get("/{note_id}", response_model=Note)
def read_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = note_service.get_note(db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=Note)
def update_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db)
):
    # Normalize note body field
    if hasattr(note, 'note_text'):
        note.body = note.note_text
    elif hasattr(note, 'note_body'):
        note.body = note.note_body
    
    db_note = note_service.update_note(db, note_id=note_id, note=note)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = note_service.delete_note(db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"} 
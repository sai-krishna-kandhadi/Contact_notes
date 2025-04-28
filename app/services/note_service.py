from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Note
from app.schemas.note import NoteCreate, NoteUpdate

def get_notes(db: Session, skip: int = 0, limit: int = 100) -> List[Note]:
    return db.query(Note).offset(skip).limit(limit).all()

def get_note(db: Session, note_id: int) -> Optional[Note]:
    return db.query(Note).filter(Note.id == note_id).first()

def create_note(db: Session, note: NoteCreate) -> Note:
    db_note = Note(
        contact_id=note.contact_id,
        body=note.body
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(
    db: Session,
    note_id: int,
    note: NoteUpdate
) -> Optional[Note]:
    db_note = get_note(db, note_id)
    if not db_note:
        return None
    
    update_data = note.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int) -> Optional[Note]:
    db_note = get_note(db, note_id)
    if not db_note:
        return None
    
    db.delete(db_note)
    db.commit()
    return db_note 
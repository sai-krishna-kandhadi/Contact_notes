from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.contact import Contact, ContactCreate, ContactUpdate
from app.services import contact_service

router = APIRouter()

@router.get("/", response_model=List[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    contacts = contact_service.get_contacts(db, skip=skip, limit=limit)
    return contacts

@router.post("/", response_model=Contact)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    return contact_service.create_contact(db=db, contact=contact)

@router.get("/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = contact_service.get_contact(db, contact_id=contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db)
):
    db_contact = contact_service.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = contact_service.delete_contact(db, contact_id=contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"} 
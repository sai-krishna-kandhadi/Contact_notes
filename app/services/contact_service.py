from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(
    db: Session,
    contact_id: int,
    contact: ContactUpdate
) -> Optional[Contact]:
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    
    update_data = contact.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    
    db.delete(db_contact)
    db.commit()
    return db_contact 
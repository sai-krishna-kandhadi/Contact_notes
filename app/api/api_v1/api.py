from fastapi import APIRouter
from app.api.api_v1.endpoints import contacts, notes

api_router = APIRouter()

api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"]) 
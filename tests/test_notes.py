from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import get_db
from app.db.models import Note, Contact

client = TestClient(app)

def test_create_note():
    # First create a contact
    contact_response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "Note",
            "last_name": "Test",
            "email": "note.test@example.com",
            "phone": "1234567890"
        }
    )
    contact_id = contact_response.json()["id"]
    
    # Test with normalized field name
    response = client.post(
        "/api/v1/notes/",
        json={
            "contact_id": contact_id,
            "body": "This is a test note"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["body"] == "This is a test note"
    assert data["contact_id"] == contact_id
    
    # Test with alternative field names
    response = client.post(
        "/api/v1/notes/",
        json={
            "contact_id": contact_id,
            "note_text": "This is another test note"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["body"] == "This is another test note"
    
    response = client.post(
        "/api/v1/notes/",
        json={
            "contact_id": contact_id,
            "note_body": "This is yet another test note"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["body"] == "This is yet another test note"

def test_read_notes():
    response = client.get("/api/v1/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_note():
    # First create a contact and note
    contact_response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "Read",
            "last_name": "Test",
            "email": "read.test@example.com",
            "phone": "1234567890"
        }
    )
    contact_id = contact_response.json()["id"]
    
    note_response = client.post(
        "/api/v1/notes/",
        json={
            "contact_id": contact_id,
            "body": "Test note for reading"
        }
    )
    note_id = note_response.json()["id"]
    
    # Then read it
    response = client.get(f"/api/v1/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["body"] == "Test note for reading" 
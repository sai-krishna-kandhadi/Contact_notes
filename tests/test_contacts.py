from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import get_db
from app.db.models import Contact

client = TestClient(app)

def test_create_contact():
    response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert data["phone"] == "1234567890"

def test_read_contacts():
    response = client.get("/api/v1/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_contact():
    # First create a contact
    create_response = client.post(
        "/api/v1/contacts/",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "9876543210"
        }
    )
    contact_id = create_response.json()["id"]
    
    # Then read it
    response = client.get(f"/api/v1/contacts/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["email"] == "test@example.com" 
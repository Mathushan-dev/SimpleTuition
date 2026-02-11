import os
import uuid
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient


@pytest.fixture
def client():
    os.environ.setdefault("MONGODB_URI", os.environ.get("MONGODB_URI") or "mongodb://localhost:27017")
    os.environ.setdefault("MONGODB_DB", "tuition_test")
    try:
        client = MongoClient(os.environ["MONGODB_URI"])
        client.admin.command("ping")
    except Exception:
        pytest.skip("MongoDB not available for tests")
    from main import app
    return TestClient(app)


def test_register_and_login(client):
    # register a user
    uid = uuid.uuid4().int % 1000000
    email = f"testuser+{uid}@example.com"
    resp = client.post("/register", json={"user_id": uid, "name": "Test User", "email": email, "password": "testpass", "user_type": "student"})
    assert resp.status_code == 201

    # login (form)
    resp2 = client.post("/login", data={"email": email, "password":"testpass"}, follow_redirects=False)
    assert resp2.status_code in (303, 200)

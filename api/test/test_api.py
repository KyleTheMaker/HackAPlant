import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from uuid import uuid4
from datetime import datetime
import sys
import os

# Add root folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from src.v1.apiRouter import get_session
from src.v1.schemas.model import Devices, Telemetry

# Setup test SQLite database
sqlite_url = "sqlite:///./test.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session_override():
    with Session(engine) as session:
        yield session


# Override the database session dependency to use the in-memory db
app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture(name="session")
def session_fixture():
    # Create the tables before each test
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Drop them after the test is done to ensure clean slate
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="test_device_id")
def test_device_id_fixture():
    return uuid4()


def test_register_device(session: Session, test_device_id):
    response = client.post(f"/v1/device/register?device_id={test_device_id}")
    assert response.status_code == 201
    assert response.json() == {"message": "device registered"}

    device_in_db = session.get(Devices, test_device_id)
    assert device_in_db is not None


def test_register_device_already_exists(session: Session, test_device_id):
    client.post(f"/v1/device/register?device_id={test_device_id}")
    response = client.post(f"/v1/device/register?device_id={test_device_id}")
    assert response.status_code == 409


def test_unregister_device(session: Session, test_device_id):
    client.post(f"/v1/device/register?device_id={test_device_id}")
    response = client.delete(f"/v1/device/unregister/{test_device_id}")
    assert response.status_code == 200

    device_in_db = session.get(Devices, test_device_id)
    assert device_in_db is None


def test_unregister_nonexistent_device(session: Session, test_device_id):
    response = client.delete(f"/v1/device/unregister/{test_device_id}")
    assert response.status_code == 404


def test_register_data(session: Session, test_device_id):
    client.post(f"/v1/device/register?device_id={test_device_id}")

    payload = {
        "device_id": str(test_device_id),
        "temperature": 25.5,
        "humidity": 60.0,
        "timestamp": datetime.now().isoformat(),
    }
    response = client.post(f"/v1/device/{test_device_id}/entry", json=payload)
    assert response.status_code == 201


def test_get_user_data(session: Session, test_device_id):
    client.post(f"/v1/device/register?device_id={test_device_id}")

    payload = {
        "device_id": str(test_device_id),
        "temperature": 22.0,
        "humidity": 50.0,
        "timestamp": datetime.now().isoformat(),
    }
    client.post(f"/v1/device/{test_device_id}/entry", json=payload)

    response = client.get(f"/v1/user/{test_device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["temperature"] == 22.0
    assert data["humidity"] == 50.0

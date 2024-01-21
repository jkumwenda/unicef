# pip install pytest pytest-asyncio

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.main import app, get_db
import pytest

# Use a testing database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

# Sample data for testing
sample_organisation = {
    "organisation": "Test Org",
    "contract_address": "0xTestAddress",
}

# Test Client
client = TestClient(app)


def test_create_organisation():
    response = client.post("/organisations/", json=sample_organisation)
    assert response.status_code == 200
    assert response.json() == sample_organisation

    # Verify organisation was added to the database
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM organisation").fetchone()
        assert result["organisation"] == sample_organisation["organisation"]
        assert result["contract_address"] == sample_organisation["contract_address"]


def test_get_organisation():
    # Create an organisation
    response_create = client.post("/organisations/", json=sample_organisation)
    assert response_create.status_code == 200

    # Get the created organisation
    organisation_id = response_create.json()["id"]
    response_get = client.get(f"/organisations/{organisation_id}")
    assert response_get.status_code == 200
    assert response_get.json()["organisation"] == sample_organisation["organisation"]


def test_update_organisation():
    # Create an organisation
    response_create = client.post("/organisations/", json=sample_organisation)
    assert response_create.status_code == 200

    # Update the created organisation
    organisation_id = response_create.json()["id"]
    updated_data = {
        "organisation": "Updated Org",
        "contract_address": "0xUpdatedAddress",
    }
    response_update = client.put(f"/organisations/{organisation_id}", json=updated_data)
    assert response_update.status_code == 200
    assert response_update.json() == updated_data

    # Verify organisation was updated in the database
    with engine.connect() as connection:
        result = connection.execute(
            f"SELECT * FROM organisation WHERE id = {organisation_id}"
        ).fetchone()
        assert result["organisation"] == updated_data["organisation"]
        assert result["contract_address"] == updated_data["contract_address"]


def test_delete_organisation():
    # Create an organisation
    response_create = client.post("/organisations/", json=sample_organisation)
    assert response_create.status_code == 200

    # Delete the created organisation
    organisation_id = response_create.json()["id"]
    response_delete = client.delete(f"/organisations/{organisation_id}")
    assert response_delete.status_code == 200

    # Verify organisation was deleted from the database
    with engine.connect() as connection:
        result = connection.execute(
            f"SELECT * FROM organisation WHERE id = {organisation_id}"
        ).fetchone()
        assert result is None


def test_get_organisations():
    # Create multiple organisations
    client.post(
        "/organisations/", json={"organisation": "Org1", "contract_address": "0x1"}
    )
    client.post(
        "/organisations/", json={"organisation": "Org2", "contract_address": "0x2"}
    )
    client.post(
        "/organisations/", json={"organisation": "Org3", "contract_address": "0x3"}
    )

    # Get the list of organisations
    response = client.get("/organisations/")
    assert response.status_code == 200

    # Assuming the response is a JSON with "data" field
    data = response.json()["data"]
    assert len(data) == 3  # Assuming three organisations were created


# Run the tests using `pytest` command in the terminal
# For example: pytest test_app.py

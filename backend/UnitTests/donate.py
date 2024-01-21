from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app, get_db
from models import Base, Donation

# Replace this with your actual contract address and private key
contract_address = "0x1aFfe7fb447D37578C1Dd3df305989b1F5198A23"
private_key = "YOUR_PRIVATE_KEY"

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Override get_db dependency to use the testing database
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

client = TestClient(app)


def test_donate_endpoint():
    # Test invalid donation amount
    response = client.post("/donate", json={"amount": 0, "account": "test"})
    assert response.status_code == 400
    assert "Donation amount must be greater than 0" in response.text

    # Test successful donation
    response = client.post(
        "/donate",
        json={
            "amount": 1.0,
            "account": "test",
            "private_key": private_key,
            "organisation_id": 1,
        },
    )
    assert response.status_code == 200
    assert "Donation successful" in response.text

    # Check if donation is recorded in the database
    with TestSessionLocal() as session:
        donation = session.query(Donation).first()
        assert donation is not None
        assert donation.amount == 1.0
        assert donation.organisation_id == 1


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.main import app, get_db
import pytest
from web3 import Web3

# Use a testing database
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

# Test Client
client = TestClient(app)

# Ganache settings
GANACHE_URL = "http://127.0.0.1:7545"
GANACHE_PRIVATE_KEY = "your_ganache_private_key"
CONTRACT_ADDRESS = "your_test_contract_address"

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Sample data for testing
sample_donation = {
    "organisation_id": 1,
    "amount": 10.0,
    "account": "0xTestAccount",
    "private_key": "0xTestPrivateKey",
}

def deploy_test_contract():
    # Implement contract deployment logic here using web3.py
    # For example, compile and deploy a test contract using solc and web3.py

# Deploy the test contract before running the tests
deploy_test_contract()

def test_donate():
    # Make a donation request
    response = client.post("/donate/", json=sample_donation)

    # Validate the response
    assert response.status_code == 200
    assert response.json()["message"] == "Donation successful"

    # Verify the donation was added to the database
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM donation").fetchone()
        assert result["organisation_id"] == sample_donation["organisation_id"]
        assert result["amount"] == sample_donation["amount"]
        assert result["transaction_hash"] is not None

# Run the test using `pytest` command in the terminal
# For example: pytest test_integration.py

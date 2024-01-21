from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import DonationSchema
from models import Donation, Organisation
from database import get_db
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from typing import Annotated
from web3 import Web3


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "0x1aFfe7fb447D37578C1Dd3df305989b1F5198A23"  # Replace with your deployed contract address
# contract_address = "0x4c5716c57472d5FA937fBE71BD226Db93D8fE4C3"  # Replace with your deployed contract address
contract_abi = [
    {
        "inputs": [],
        "name": "donate",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "donor",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256",
            },
        ],
        "name": "DonationMade",
        "type": "event",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "allDonations",
        "outputs": [
            {"internalType": "address", "name": "donor", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "donationCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getAllDonations",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "donor", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                ],
                "internalType": "struct DonationContract.Donation[]",
                "name": "",
                "type": "tuple[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "senderAddress",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def get_web3():
    if not w3.is_connected():
        raise HTTPException(status_code=500, detail="Ethereum node connection error")
    return w3


@router.post("/")
async def donate(
    donation_schema: DonationSchema,
    db: Session = Depends(get_db),
):
    # Validate donation amount
    if donation_schema.amount <= 0:
        raise HTTPException(
            status_code=400, detail="Donation amount must be greater than 0"
        )

    # Donate to the smart contract
    try:
        nonce = w3.eth.get_transaction_count(donation_schema.account)
        gas_price = w3.eth.gas_price
        gas_limit = 6721975

        transaction = {
            "from": donation_schema.account,
            "to": contract_address,
            "value": w3.to_wei(donation_schema.amount, "ether"),
            "gas": gas_limit,
            "gasPrice": gas_price,
            "nonce": nonce,
        }

        signed_transaction = w3.eth.account.sign_transaction(
            transaction, donation_schema.private_key
        )
        transaction_hash = w3.eth.send_raw_transaction(
            signed_transaction.rawTransaction
        )

        donation_model = Donation(
            organisation_id=donation_schema.organisation_id,
            amount=donation_schema.amount,
            transaction_hash=transaction_hash.hex(),
        )
        db.add(donation_model)
        db.commit()

        return {
            "message": "Donation successful",
            "transaction_hash": transaction_hash.hex(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error donating to smart contract: {e}"
        )

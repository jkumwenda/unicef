from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from schemas.schemas import DonationSchema
from models import Donation
from database import get_db
from ethereum_config import contract_abi, w3, contract_address
from web3 import Web3


router = APIRouter(
    responses={404: {"description": "Not found"}},
)

w3 = w3
contract_address = contract_address
contract_abi = contract_abi


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

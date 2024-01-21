from pydantic import BaseModel, EmailStr


class OrganisationSchema(BaseModel):
    organisation: str
    contract_address: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "organisation": "Chifundo cha onse",
                "contract_address": "0x0DD5CbCcd2872D5b8A2220dA9967A7629E2Fa22e",
            }
        }


class DonationSchema(BaseModel):
    organisation_id: int
    account: str
    amount: float
    private_key: str

    class Config:
        validate_default = True
        json_schema_extra = {
            "example": {
                "organisation_id": 1,
                "account": "0x0DD5CbCcd2872D5b8A2220dA9967A7629E2Fa22e",
                "amount": 1.0,
                "private_key": "0x9201268b0afe1ad0952f38accea83356d031786fb9f3e8a556b0b6626b347f16",
            }
        }

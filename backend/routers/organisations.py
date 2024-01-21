from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.schemas import OrganisationSchema
from models import Organisation, Donation
from database import get_db
import math
from sqlalchemy import or_, func

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


def get_object(organisation_id, db):
    organisation = (
        db.query(Organisation).filter(Organisation.id == organisation_id).first()
    )
    if organisation is None:
        raise HTTPException(
            status_code=404, detail=f"ID {organisation_id} : Does not exist"
        )
    return organisation


@router.get("/")
async def get_organisations(
    db: Session = Depends(get_db),
    skip: int = Query(default=1, ge=1),
    limit: int = 10,
    search: str = "",
):
    offset = (skip - 1) * limit

    # Join Organisation and Donation tables and perform a group by
    query = (
        db.query(Organisation, func.sum(Donation.amount).label("total_amount"))
        .outerjoin(Donation, Organisation.id == Donation.organisation_id)
        .filter(or_(Organisation.organisation.ilike(f"%{search}%")))
        .group_by(
            Organisation.id,
            Organisation.organisation,
            Organisation.contract_address,
            Organisation.created_at,
            Organisation.updated_at,
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_count = (
        db.query(Organisation)
        .filter(or_(Organisation.organisation.ilike(f"%{search}%")))
        .count()
    )
    pages = math.ceil(total_count / limit)

    # Extract the relevant data and create the response
    result = [
        {
            "id": org.id,
            "organisation": org.organisation,
            "contract_address": org.contract_address,
            "created_at": org.created_at,
            "updated_at": org.updated_at,
            "total_amount": total_amount,
        }
        for org, total_amount in query
    ]

    return {"pages": pages, "data": result}


@router.post("/")
async def add_organisation(
    organisation_schema: OrganisationSchema,
    db: Session = Depends(get_db),
):
    organisation_model = Organisation(
        organisation=organisation_schema.organisation,
        contract_address=organisation_schema.contract_address,
    )

    db.add(organisation_model)
    db.commit()

    return organisation_schema


@router.get("/{organisation_id}")
async def get_organisation(
    organisation_id: int,
    db: Session = Depends(get_db),
):
    return get_object(organisation_id, db)


@router.put("/{organisation_id}")
async def update_organisation(
    organisation_id: int,
    organisation_schema: OrganisationSchema,
    db: Session = Depends(get_db),
):
    organisation_model = get_object(organisation_id, db)
    organisation_model.organisation = (organisation_schema.organisation,)
    organisation_model.contract_address = organisation_schema.contract_address
    db.add(organisation_model)
    db.commit()

    return organisation_schema


@router.delete("/{organisation_id}")
async def delete_organisation(
    organisation_id: int,
    db: Session = Depends(get_db),
):
    get_object(organisation_id, db)
    db.query(Organisation).filter(Organisation.id == organisation_id).delete()
    db.commit()

    raise HTTPException(status_code=200, detail="Organisation Successfully deleted")

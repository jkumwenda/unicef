from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Float,
    TIMESTAMP,
    text,
)
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Organisation(Base):
    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, index=True)
    organisation = Column(String(255), nullable=False, unique=True)
    contract_address = Column(String(255), nullable=False, unique=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.now,
    )

    donation = relationship("Donation", back_populates="organisation")

    def __repr__(self):
        return f"<Organisation {self.organisation}"


class Donation(Base):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True)
    organisation_id = Column(Integer, ForeignKey("organisation.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_hash = Column(String(255), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    organisation = relationship("Organisation", back_populates="donation")

    def __repr__(self):
        return f"<Donation {self.amount} >"

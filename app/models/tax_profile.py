from sqlalchemy import Column, Integer, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase, TimestampMixin
import enum

class ActivityType(str, enum.Enum):
    individual_activity = "individual_activity"
    business_certificate = "business_certificate"

class TaxProfile(UUIDBase, TimestampMixin, Base):
    __tablename__ = "tax_profiles"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    tax_year = Column(Integer, nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    expense_method = Column(String, nullable=False, default="actual")
    vat_status = Column(
        Enum("non_payer", "payer", name="vat_status"),
        nullable=False,
    )

    user = relationship("User", back_populates="tax_profiles")


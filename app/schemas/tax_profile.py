from enum import Enum
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ActivityType(str, Enum):
    individual_activity = "individual_activity"
    business_certificate = "business_certificate"

class VatStatus(str, Enum):
    non_payer = "non_payer"
    payer = "payer"

class TaxProfileCreate(BaseModel):
    tax_year: int
    activity_type: ActivityType
    expense_method: str = "actual"
    vat_status: VatStatus

class TaxProfileUpdate(BaseModel):
    tax_year: Optional[int] = None
    activity_type: Optional[ActivityType] = None
    expense_method: Optional[str] = None
    vat_status: Optional[VatStatus] = None

class TaxProfileOut(BaseModel):
    id: UUID
    tax_year: int
    activity_type: ActivityType
    expense_method: str
    vat_status: VatStatus

    class Config:
        from_attributes = True

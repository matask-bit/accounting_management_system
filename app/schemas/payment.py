from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional


class PaymentCreate(BaseModel):
    invoice_id: UUID
    payment_date: date
    amount: float = Field(gt=0)

class PaymentUpdate(BaseModel):
    invoice_id: Optional[UUID] = None
    payment_date: Optional[date] = None
    amount: Optional[float] = Field(default=None, gt=0)


class PaymentOut(BaseModel):
    id: UUID
    invoice_id: UUID
    payment_date: date
    amount: float

    class Config:
        from_attributes = True

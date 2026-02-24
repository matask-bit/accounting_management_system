from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class InvoiceLineCreate(BaseModel):
    description: str
    quantity: int = Field(default=1, gt=0)
    unit_price: float
    vat_rate: float = Field(default=0, ge=0)

class InvoiceLineUpdate(BaseModel):
    description: Optional[str] = None
    quantity: Optional[int] = Field(default=None, gt=0)
    unit_price: Optional[float] = None
    vat_rate: Optional[float] = Field(default=None, ge=0)


class InvoiceLineOut(BaseModel):
    id: UUID
    invoice_id: UUID
    description: str
    quantity: int
    unit_price: float
    vat_rate: float
    line_subtotal: float
    vat_amount: float
    line_total: float

    class Config:
        from_attributes = True

from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class InvoiceCreate(BaseModel):
    client_id: UUID
    number: str
    issue_date: date
    due_date: Optional[date] = None

class InvoiceUpdate(BaseModel):
    client_id: Optional[UUID] = None
    number: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None


class InvoiceOut(BaseModel):
    id: UUID
    client_id: UUID
    number: str
    issue_date: date
    due_date: Optional[date]
    status: str
    subtotal: float
    vat_total: float
    total: float

    class Config:
        from_attributes = True

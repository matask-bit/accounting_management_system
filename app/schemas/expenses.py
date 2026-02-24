from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional


class ExpenseCreate(BaseModel):
    description: Optional[str] = None
    amount: float = Field(gt=0)
    expense_date: date

class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    expense_date: Optional[date] = None


class ExpenseOut(BaseModel):
    id: UUID
    description: Optional[str]
    expense_date: date
    amount: float

    class Config:
        from_attributes = True

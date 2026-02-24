from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class RevenueSource(BaseModel):
    id: UUID
    number: str
    issue_date: date
    total: float

class ExpenseSource(BaseModel):
    id: UUID
    description: Optional[str]
    expense_date: date
    amount: float

class TaxSummaryOut(BaseModel):
    tax_profile_id: UUID
    tax_year: int
    activity_type: str
    revenue: float
    expenses: float
    profit: float
    gpm: float
    vsd: float
    psd: float
    total_taxes: float

class TaxSummaryExplainOut(TaxSummaryOut):
    revenue_sources: list[RevenueSource]
    expense_sources: list[ExpenseSource]
    assumptions: list[str]
    formulas: list[str]

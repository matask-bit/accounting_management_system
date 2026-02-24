from pydantic import BaseModel

class DashboardSummaryOut(BaseModel):
    total_income: float
    total_expenses: float
    profit: float
    estimated_taxes: float

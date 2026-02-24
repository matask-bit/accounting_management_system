from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.schemas.dashboard import DashboardSummaryOut
from app.services.tax import calculate_tax_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DashboardSummaryOut)
def dashboard_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    summary = calculate_tax_summary(db, user.id)
    if not summary:
        raise HTTPException(status_code=400, detail="Tax profile not found")

    return {
        "total_income": summary["revenue"],
        "total_expenses": summary["expenses"],
        "profit": summary["profit"],
        "estimated_taxes": summary["total_taxes"],
    }

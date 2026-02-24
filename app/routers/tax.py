from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.schemas.tax_summary import TaxSummaryOut, TaxSummaryExplainOut
from app.services.tax import calculate_tax_summary, calculate_tax_summary_explain

router = APIRouter(prefix="/tax", tags=["tax"])

@router.get("/summary", response_model=TaxSummaryOut)
def tax_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    summary = calculate_tax_summary(db, user.id)
    if not summary:
        raise HTTPException(status_code=400, detail="Tax profile not found")
    return summary

@router.get("/summary/explain", response_model=TaxSummaryExplainOut)
def tax_summary_explain(db: Session = Depends(get_db), user=Depends(get_current_user)):
    summary = calculate_tax_summary_explain(db, user.id)
    if not summary:
        raise HTTPException(status_code=400, detail="Tax profile not found")
    return summary

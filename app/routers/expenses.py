from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_current_user, get_db
from app.models.expense import Expense
from app.schemas.expenses import ExpenseCreate, ExpenseOut, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    expense = Expense(user_id=user.id, **data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

@router.get("/", response_model=list[ExpenseOut])
def list_expenses(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Expense).filter(Expense.user_id == user.id).all()

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: UUID,
    data: ExpenseUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return None

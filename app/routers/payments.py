from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from decimal import Decimal

from app.core.deps import get_current_user, get_db
from app.models.invoice import Invoice, InvoiceStatus
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentOut, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == data.invoice_id, Invoice.user_id == user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status != InvoiceStatus.finalized:
        raise HTTPException(status_code=400, detail="Payments require a finalized invoice")

    payment = Payment(user_id=user.id, **data.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@router.get("/", response_model=list[PaymentOut])
def list_payments(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Payment).filter(Payment.user_id == user.id).all()

@router.put("/{payment_id}", response_model=PaymentOut)
def update_payment(
    payment_id: UUID,
    data: PaymentUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id, Payment.user_id == user.id)
        .first()
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.invoice_id is None:
        raise HTTPException(status_code=400, detail="Payment must reference an invoice")
    if payment.amount is None or Decimal(str(payment.amount)) <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be > 0")

    update_data = data.model_dump(exclude_unset=True)
    if "invoice_id" in update_data:
        invoice_id = update_data["invoice_id"]
        if invoice_id is None:
            raise HTTPException(status_code=400, detail="Payment must reference an invoice")
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id, Invoice.user_id == user.id)
            .first()
        )
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        if invoice.status != InvoiceStatus.finalized:
            raise HTTPException(status_code=400, detail="Payments require a finalized invoice")
    else:
        if payment.invoice_id is None:
            raise HTTPException(status_code=400, detail="Payment must reference an invoice")
        current_invoice = (
            db.query(Invoice)
            .filter(Invoice.id == payment.invoice_id, Invoice.user_id == user.id)
            .first()
        )
        if not current_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        if current_invoice.status != InvoiceStatus.finalized:
            raise HTTPException(status_code=400, detail="Payments require a finalized invoice")

    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    payment_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id, Payment.user_id == user.id)
        .first()
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_current_user, get_db
from app.models.client import Client
from app.models.invoice import Invoice, InvoiceStatus
from app.services.invoice import recalc_invoice_totals
from app.schemas.invoice import InvoiceCreate, InvoiceOut, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
def create_invoice(
    data: InvoiceCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = (
        db.query(Client)
        .filter(Client.id == data.client_id, Client.user_id == user.id)
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    invoice = Invoice(user_id=user.id, **data.model_dump(exclude_none=True))
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    recalc_invoice_totals(db, invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/", response_model=list[InvoiceOut])
def list_invoices(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Invoice).filter(Invoice.user_id == user.id).all()

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{invoice_id}", response_model=InvoiceOut)
def update_invoice(
    invoice_id: UUID,
    data: InvoiceUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == InvoiceStatus.finalized:
        raise HTTPException(status_code=400, detail="Invoice is finalized")

    update_data = data.model_dump(exclude_unset=True)
    if "client_id" in update_data:
        client = (
            db.query(Client)
            .filter(Client.id == update_data["client_id"], Client.user_id == user.id)
            .first()
        )
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

    for key, value in update_data.items():
        setattr(invoice, key, value)

    recalc_invoice_totals(db, invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == InvoiceStatus.finalized:
        raise HTTPException(status_code=400, detail="Finalized invoices cannot be deleted")

    db.delete(invoice)
    db.commit()
    return None

@router.post("/{invoice_id}/finalize", response_model=InvoiceOut)
def finalize_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id, Invoice.user_id == user.id)
        .first()
    )
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == InvoiceStatus.finalized:
        raise HTTPException(status_code=400, detail="Invoice already finalized")

    recalc_invoice_totals(db, invoice)
    invoice.status = InvoiceStatus.finalized
    db.commit()
    db.refresh(invoice)
    return invoice

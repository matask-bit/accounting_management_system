from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_current_user, get_db
from app.models.invoice import Invoice, InvoiceStatus
from app.models.invoice_line import InvoiceLine
from app.schemas.invoice_line import InvoiceLineCreate, InvoiceLineOut, InvoiceLineUpdate
from app.services.invoice import recalc_invoice_totals

router = APIRouter(prefix="/invoices", tags=["invoice-lines"])

@router.post("/{invoice_id}/lines", response_model=InvoiceLineOut, status_code=status.HTTP_201_CREATED)
def create_invoice_line(
    invoice_id: UUID,
    data: InvoiceLineCreate,
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

    line = InvoiceLine(invoice_id=invoice.id, **data.model_dump())
    db.add(line)
    db.commit()
    db.refresh(line)
    recalc_invoice_totals(db, invoice)
    db.commit()
    return line

@router.get("/{invoice_id}/lines", response_model=list[InvoiceLineOut])
def list_invoice_lines(
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
        raise HTTPException(status_code=400, detail="Invoice is finalized")

    return db.query(InvoiceLine).filter(InvoiceLine.invoice_id == invoice.id).all()

@router.put("/{invoice_id}/lines/{line_id}", response_model=InvoiceLineOut)
def update_invoice_line(
    invoice_id: UUID,
    line_id: UUID,
    data: InvoiceLineUpdate,
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

    line = (
        db.query(InvoiceLine)
        .filter(InvoiceLine.id == line_id, InvoiceLine.invoice_id == invoice.id)
        .first()
    )
    if not line:
        raise HTTPException(status_code=404, detail="Invoice line not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(line, key, value)

    db.commit()
    db.refresh(line)
    recalc_invoice_totals(db, invoice)
    db.commit()
    return line

@router.delete("/{invoice_id}/lines/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice_line(
    invoice_id: UUID,
    line_id: UUID,
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

    line = (
        db.query(InvoiceLine)
        .filter(InvoiceLine.id == line_id, InvoiceLine.invoice_id == invoice.id)
        .first()
    )
    if not line:
        raise HTTPException(status_code=404, detail="Invoice line not found")

    db.delete(line)
    db.commit()
    recalc_invoice_totals(db, invoice)
    db.commit()
    return None

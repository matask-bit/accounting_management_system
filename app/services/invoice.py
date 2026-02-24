from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine

def _to_decimal(value, default="0"):
    if value is None:
        return Decimal(default)
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))

def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))

def recalc_invoice_totals(db: Session, invoice: Invoice) -> dict:
    lines = db.query(InvoiceLine).filter(InvoiceLine.invoice_id == invoice.id).all()
    subtotal = sum((_to_decimal(line.line_subtotal) for line in lines), Decimal("0"))
    vat_total = sum((_to_decimal(line.vat_amount) for line in lines), Decimal("0"))
    total = subtotal + vat_total

    invoice.total = _money(total)
    return {
        "subtotal": _money(subtotal),
        "vat_total": _money(vat_total),
        "total": _money(total),
    }

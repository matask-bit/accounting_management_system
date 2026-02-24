from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.tax_profile import TaxProfile
from app.models.invoice import Invoice, InvoiceStatus
from app.models.expense import Expense

# Assumptions:
# - Cash basis: revenue is based on finalized invoice totals, not payment dates.
# - VAT: invoice totals include VAT; revenue is gross (VAT included).
# - Expenses: all expenses are treated as deductible, no 30% method applied.
# - Rates are estimates only and not filing-ready.

def _to_decimal(value, default="0"):
    if value is None:
        return Decimal(default)
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))

def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"))

RATES = {
    "individual_activity": {
        "gpm": Decimal("0.15"),
        "vsd": Decimal("0.1252"),
        "psd": Decimal("0.0698"),
    },
    "business_certificate": {
        "gpm": Decimal("0.05"),
        "vsd": Decimal("0.00"),
        "psd": Decimal("0.00"),
    },
}

def get_latest_tax_profile(db: Session, user_id):
    return (
        db.query(TaxProfile)
        .filter(TaxProfile.user_id == user_id)
        .order_by(TaxProfile.tax_year.desc())
        .first()
    )

def calculate_tax_summary(db: Session, user_id):
    tax_profile = get_latest_tax_profile(db, user_id)
    if not tax_profile:
        return None

    revenue = (
        db.query(Invoice)
        .filter(Invoice.user_id == user_id, Invoice.status == InvoiceStatus.finalized)
        .all()
    )
    revenue_total = sum((_to_decimal(inv.total) for inv in revenue), Decimal("0"))

    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    expense_total = sum((_to_decimal(exp.amount) for exp in expenses), Decimal("0"))

    profit = revenue_total - expense_total
    taxable_base = profit if profit > 0 else Decimal("0")

    rates = RATES.get(tax_profile.activity_type.value, RATES["individual_activity"])
    gpm = taxable_base * rates["gpm"]
    vsd = taxable_base * rates["vsd"]
    psd = taxable_base * rates["psd"]
    total_taxes = gpm + vsd + psd

    return {
        "tax_profile_id": tax_profile.id,
        "tax_year": tax_profile.tax_year,
        "activity_type": tax_profile.activity_type.value,
        "revenue": _money(revenue_total),
        "expenses": _money(expense_total),
        "profit": _money(profit),
        "gpm": _money(gpm),
        "vsd": _money(vsd),
        "psd": _money(psd),
        "total_taxes": _money(total_taxes),
    }

def calculate_tax_summary_explain(db: Session, user_id):
    summary = calculate_tax_summary(db, user_id)
    if not summary:
        return None

    revenue_invoices = (
        db.query(Invoice)
        .filter(Invoice.user_id == user_id, Invoice.status == InvoiceStatus.finalized)
        .all()
    )
    expense_items = db.query(Expense).filter(Expense.user_id == user_id).all()

    assumptions = [
        "Revenue uses finalized invoices only (drafts excluded).",
        "Revenue is gross: invoice totals include VAT.",
        "Expenses are treated as fully deductible (no 30% method).",
        "Tax rates are estimates and not filing-ready.",
    ]

    formulas = [
        "profit = revenue - expenses",
        "taxable_base = max(profit, 0)",
        "gpm = taxable_base * gpm_rate",
        "vsd = taxable_base * vsd_rate",
        "psd = taxable_base * psd_rate",
        "total_taxes = gpm + vsd + psd",
    ]

    summary["revenue_sources"] = [
        {
            "id": inv.id,
            "number": inv.number,
            "issue_date": inv.issue_date,
            "total": _money(_to_decimal(inv.total)),
        }
        for inv in revenue_invoices
    ]
    summary["expense_sources"] = [
        {
            "id": exp.id,
            "description": exp.description,
            "expense_date": exp.expense_date,
            "amount": _money(_to_decimal(exp.amount)),
        }
        for exp in expense_items
    ]
    summary["assumptions"] = assumptions
    summary["formulas"] = formulas
    return summary

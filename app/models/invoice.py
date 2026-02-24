from sqlalchemy import Column, String, ForeignKey, Numeric, Date, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase, TimestampMixin
from decimal import Decimal
import enum

class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    finalized = "finalized"

class Invoice(UUIDBase, TimestampMixin, Base):
    __tablename__ = "invoices"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    client_id = Column(ForeignKey("clients.id"), nullable=False)
    number = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date)
    status = Column(Enum(InvoiceStatus, name="invoice_status"), nullable=False, default=InvoiceStatus.draft)
    total = Column(Numeric(10, 2), default=0)

    user = relationship("User", back_populates="invoices")
    client = relationship("Client", back_populates="invoices")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete")

    def _to_decimal(self, value, default="0"):
        if value is None:
            return Decimal(default)
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    @property
    def subtotal(self):
        return sum((line.line_subtotal for line in self.lines), Decimal("0"))

    @property
    def vat_total(self):
        return sum((line.vat_amount for line in self.lines), Decimal("0"))

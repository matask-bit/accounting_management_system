from sqlalchemy import Column, String, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase
from decimal import Decimal

class InvoiceLine(UUIDBase, Base):
    __tablename__ = "invoice_lines"

    invoice_id = Column(ForeignKey("invoices.id"), nullable=False)
    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Numeric(10, 2))
    vat_rate = Column(Numeric(5, 2), default=0)

    invoice = relationship("Invoice", back_populates="lines")

    def _to_decimal(self, value, default="0"):
        if value is None:
            return Decimal(default)
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    @property
    def line_subtotal(self):
        qty = self._to_decimal(self.quantity)
        unit = self._to_decimal(self.unit_price)
        return qty * unit

    @property
    def vat_amount(self):
        rate = self._to_decimal(self.vat_rate)
        return self.line_subtotal * (rate / Decimal("100"))

    @property
    def line_total(self):
        return self.line_subtotal + self.vat_amount

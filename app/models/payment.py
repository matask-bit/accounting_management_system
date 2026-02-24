from sqlalchemy import Column, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase, TimestampMixin

class Payment(UUIDBase, TimestampMixin, Base):
    __tablename__ = "payments"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    invoice_id = Column(ForeignKey("invoices.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date)

    user = relationship("User", back_populates="payments")

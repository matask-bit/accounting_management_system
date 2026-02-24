from sqlalchemy import Column, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase, TimestampMixin

class Expense(UUIDBase, TimestampMixin, Base):
    __tablename__ = "expenses"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    description = Column(String)
    amount = Column(Numeric(10, 2))
    expense_date = Column(Date)

    user = relationship("User", back_populates="expenses")



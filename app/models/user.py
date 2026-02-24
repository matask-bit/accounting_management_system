from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase, TimestampMixin

class User(UUIDBase, TimestampMixin, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    locale = Column(String, default="lt")
    timezone = Column(String, default="Europe/Vilnius")

    tax_profiles = relationship("TaxProfile", back_populates="user")
    clients = relationship("Client", back_populates="user")
    invoices = relationship("Invoice", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    expenses = relationship("Expense", back_populates="user")

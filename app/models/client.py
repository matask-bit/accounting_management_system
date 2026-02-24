from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDBase, TimestampMixin

class Client(UUIDBase, TimestampMixin, Base):
    __tablename__ = "clients"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    country_code = Column(String(2), nullable=False)
    vat_id = Column(String)
    email = Column(String)
    address = Column(String)

    user = relationship("User", back_populates="clients")
    invoices = relationship("Invoice", back_populates="client")

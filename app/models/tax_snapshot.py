from sqlalchemy import Column, Integer, Numeric, Enum, ForeignKey

from app.database import Base
from app.models.base import UUIDBase, TimestampMixin

class TaxSnapshot(UUIDBase, TimestampMixin, Base):
    __tablename__ = "tax_snapshots"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    tax_year = Column(Integer, nullable=False)

    period = Column(
        Enum("month", "year", name="tax_period"),
        nullable=False,
    )
    period_index = Column(Integer, nullable=False)

    income_total = Column(Numeric(12, 2), default=0)
    expense_total = Column(Numeric(12, 2), default=0)
    profit = Column(Numeric(12, 2), default=0)

    gpm_est = Column(Numeric(12, 2), default=0)
    vsd_est = Column(Numeric(12, 2), default=0)
    psd_est = Column(Numeric(12, 2), default=0)

from sqlalchemy import Column, String, Enum, ForeignKey

from app.database import Base
from app.models.base import UUIDBase, TimestampMixin

class Attachment(UUIDBase, TimestampMixin, Base):
    __tablename__ = "attachments"

    user_id = Column(ForeignKey("users.id"), nullable=False)

    entity_type = Column(
        Enum("invoice", "expense", "client", "other", name="attachment_entity"),
        nullable=False,
    )

    entity_id = Column(String)
    file_name = Column(String)
    mime_type = Column(String)
    storage_key = Column(String)

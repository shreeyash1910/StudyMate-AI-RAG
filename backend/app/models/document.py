from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Document(Base):

    __tablename__ = "Documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("Users.id"),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    page_count = Column(
        Integer,
        nullable=True
    )

    uploaded_at = Column(
        DateTime,
        server_default=func.getdate()
    )
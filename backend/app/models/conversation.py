from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Conversation(Base):

    __tablename__ = "Conversations"

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

    title = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.getdate()
    )
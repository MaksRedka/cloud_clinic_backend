from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    Float,
    DateTime,
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql

from src.database import Base


class Conversation(Base):
    """Model represents chat communications."""
    __tablename__ = "conversation"
    chat_uuid = Column(postgresql.UUID(as_uuid=True),
                          primary_key=True, unique=True)
    user_uuid = Column(postgresql.UUID(as_uuid=True),
                        ForeignKey("user.user_uuid", ondelete='CASCADE'))
    doctor_uuid = Column(postgresql.UUID(as_uuid=True),
                        ForeignKey("user.user_uuid", ondelete='CASCADE'))
    data = Column(JSON)

class Message(Base):
    """Model represents chat messages."""
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chat_uuid = Column(postgresql.UUID(as_uuid=True),
                        ForeignKey("conversation.chat_uuid", ondelete='CASCADE'))
    message = Column(Text)
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    data = Column(JSON)
    
    conversation = relationship(
        "Conversation",
        lazy="joined"
    )
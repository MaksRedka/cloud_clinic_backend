from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    Float,
    DateTime,
    JSON,
)
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects import postgresql

from src.database import Base


class User(Base):
    """Model represents chat communications."""
    __tablename__ = "user"
    user_uuid = Column(postgresql.UUID(as_uuid=True),
                          primary_key=True, unique=True)
    user_type = Column(Text)
    name = Column(Text)
    email = Column(EmailType, unique=True, index=True, nullable=False)
    password = Column(Text)
    data = Column(JSON)


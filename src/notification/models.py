from sqlalchemy import (
    Column,
    Integer,
    Text,
    JSON,

)

from src.database import Base


class Notification(Base):
    """Model represents chat communications."""
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, unique=True)
    message = Column(Text)
    type = Column(Text)
    data = Column(JSON) # shoud contain plan id, plan part and notification time etc.


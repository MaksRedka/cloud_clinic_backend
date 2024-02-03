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
from sqlalchemy.dialects import postgresql

from src.database import Base


class TreatmentPlan(Base):
    """Model represents chat communications."""
    __tablename__ = "treatment-plan"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_uuid = Column(postgresql.UUID(as_uuid=True),
                        ForeignKey("user.user_uuid", ondelete='CASCADE'))
    title = Column(Text)
    description = Column(Text)
    is_open = Column(Boolean)
    
    data = Column(JSON) # should contain plan steps and doctor


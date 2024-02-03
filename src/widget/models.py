# from sqlalchemy import (
#     Column,
#     Integer,
#     Text,
#     Boolean,
#     ForeignKey,
#     Float,
#     DateTime
# )
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from sqlalchemy.dialects import postgresql

# from src.database import Base


# class Conversation(Base):
#     """Model represents chat communications."""
#     __tablename__ = "conversation"
#     session_uuid = Column(postgresql.UUID(as_uuid=True),
#                           primary_key=True, unique=True)
#     rating = Column(Integer)
#     is_finished = Column(Boolean, default=False)

# class Message(Base):
#     """Model represents chat messages."""
#     __tablename__ = "message"
#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     session_uuid = Column(postgresql.UUID(as_uuid=True),
#                         ForeignKey("conversation.session_uuid", ondelete='CASCADE'))
#     answer_id = Column(Integer)
#     faiss_distance = Column(Float)
#     timestamp = Column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#     )

#     conversation = relationship(
#         "Conversation",
#         lazy="joined"
#     )

# class FAQ(Base):
#     """Model represents FAQ elements."""
#     __tablename__ = "faq"
#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     question = Column(Text)
#     question_wide = Column(Text)
#     child_category = Column(Text)
#     parent_category = Column(Text)
#     answer_short = Column(Text)
#     answer_full = Column(Text)


# # class Abbreviation(Base):
# #     """Model represents Abbreviation elements."""
# #     __tablename__ = "abbreviation"
# #     id = Column(Integer, primary_key=True, unique=True)
# #     abbreviation = Column(Text)
# #     deciphering = Column(Text)

# """Crud operations for communication module."""
# from typing import Type
# from uuid import UUID
# from datetime import datetime
# from fastapi import HTTPException, status

# from fastapi.encoders import jsonable_encoder
# from sqlalchemy import select, desc
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import IntegrityError
# from src.widget.models import Conversation, Message


# async def create_conversation(
#     db: AsyncSession,
#     session_uuid: UUID,
#     rating: int,
#     is_finished: bool
# ) -> Conversation:
#     """Create conversation in database."""
#     conv: Conversation = Conversation(
#         session_uuid=session_uuid,
#         rating=rating,
#         is_finished=is_finished
#     )
    
#     db.add(conv)

#     try:
#         await db.commit()
#         await db.refresh(conv)
#         return conv
#     except IntegrityError as ex:
#         await db.rollback()
#         print(ex)
#         raise HTTPException(
#             detail={"message": "Conversation can not be created"},
#             status_code=status.HTTP_400_BAD_REQUEST
#         )
    
# async def update_conversation(
#     db: AsyncSession,
#     session_uuid: UUID,
#     rating: int,
#     is_finished: bool
# ) -> Conversation:
#     """Update conversation in database."""
#     conv: Conversation = await get_conversation_by_session_id(db=db, session_id=session_uuid)
#     conv.rating = rating
#     conv.is_finished = is_finished

#     try:
#         await db.commit()
#         await db.refresh(conv)
#         return conv
#     except IntegrityError as ex:
#         await db.rollback()
#         print(ex)
#         raise HTTPException(detail="Conversation can not be updated",
#                             status_code=status.HTTP_400_BAD_REQUEST)
    
# async def create_message(
#     db: AsyncSession,
#     session_uuid: UUID,
#     answer_id: int,
#     faiss_distance: float,
#     ) -> Message:
#     """Create message in database."""

#     msg: Message = Message(
#         session_uuid=session_uuid,
#         answer_id=answer_id,
#         faiss_distance=faiss_distance
#     )
    
#     db.add(msg)

#     try:
#         await db.commit()
#         await db.refresh(msg)
#         return msg
#     except IntegrityError as ex:
#         await db.rollback()
#         print(ex)
#         raise HTTPException(
#             detail={"message": "Message can not be created"},
#             status_code=status.HTTP_400_BAD_REQUEST
#         )

# async def get_conversation_by_session_id(db: AsyncSession, session_id: UUID) -> Conversation:
#     """Get conversation by session id."""
#     query = await db.execute(
#         select(Conversation).filter(
#             Conversation.session_uuid == session_id))
#     conv: Conversation = query.scalars().first()
#     return conv

# async def list_messages_by_session_id(db: AsyncSession, session_id: UUID, descending: bool, sort_name: str) -> list[Type[Message]]:
#     """Get messages by session id."""
#     query = await db.execute(
#         select(Message).filter(
#             Message.session_uuid == session_id).order_by(
#             desc(getattr(Message, sort_name)) if descending
#             else getattr(Message, sort_name)
#         ))
#     return query.scalars().all()


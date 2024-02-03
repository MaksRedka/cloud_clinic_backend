from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from src.chat.models import Conversation, Message

# Conversation CRUD

# Create
async def create_conversation(db: AsyncSession, chat_uuid: str, user_uuid: str, doctor_uuid: str, data: dict):
    try:
        db_conversation = Conversation(chat_uuid=chat_uuid, user_uuid=user_uuid, doctor_uuid=doctor_uuid, data=data)
        db.add(db_conversation)
        await db.commit()
        await db.refresh(db_conversation)
        return db_conversation
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error creating conversation: {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Read
async def get_conversation(db: AsyncSession, chat_uuid: str):
    result = await db.execute(select(Conversation).filter(Conversation.chat_uuid == chat_uuid))
    return result.scalar()

async def get_all_conversations(db: AsyncSession):
    result = await db.execute(select(Conversation))
    return result.scalars().all()

async def get_messages_for_conversation(db: AsyncSession, chat_uuid: str):
    result = await db.execute(
        select(Message)
        .options(joinedload(Message.conversation))
        .filter(Message.chat_uuid == chat_uuid)
    )
    return result.scalars().all()

# Update
async def update_conversation(db: AsyncSession, chat_uuid: str, data: dict):
    try:
        result = await db.execute(update(Conversation).where(Conversation.chat_uuid == chat_uuid).values(data))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error updating conversation: {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Delete
async def delete_conversation(db: AsyncSession, chat_uuid: str):
    try:
        result = await db.execute(delete(Conversation).where(Conversation.chat_uuid == chat_uuid))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error deleting conversation: {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Message CRUD

# Create
async def create_message(db: AsyncSession, chat_uuid: str, data: dict):
    try:
        db_message = Message(chat_uuid=chat_uuid, data=data)
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        return db_message
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error creating message {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Read
async def get_message(db: AsyncSession, message_id: int):
    result = await db.execute(select(Message).filter(Message.id == message_id))
    return result.scalar()

async def get_all_messages(db: AsyncSession):
    result = await db.execute(select(Message))
    return result.scalars().all()

# Update
async def update_message(db: AsyncSession, message_id: int, data: dict):
    try:
        result = await db.execute(update(Message).where(Message.id == message_id).values(data))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error updating message: {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Delete
async def delete_message(db: AsyncSession, message_id: int):
    try:
        result = await db.execute(delete(Message).where(Message.id == message_id))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error deleting message: {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

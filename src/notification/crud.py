from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from src.notification.models import Notification
from fastapi import HTTPException, status

# Create
async def create_notification(db: AsyncSession, message: str, type: str, data: dict):
    try:
        async with db.begin():
            db_notification = Notification(message=message, type=type, data=data)
            db.add(db_notification)
            await db.commit()
            await db.refresh(db_notification)
        return db_notification
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Повідомлення з помилкою {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Read
async def get_notification(db: AsyncSession, notification_id: int):
    result = await db.execute(select(Notification).filter(Notification.id == notification_id))
    return result.scalar()

async def get_all_notifications(db: AsyncSession):
    result = await db.execute(select(Notification))
    return result.scalars().all()

# Update
async def update_notification(db: AsyncSession, notification_id: int, data: dict):
    try:
        async with db.begin():
            result = await db.execute(update(Notification).where(Notification.id == notification_id).values(data))
            await db.commit()
            return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Повідомлення з помилкою {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Delete
async def delete_notification(db: AsyncSession, notification_id: int):
    try:
        async with db.begin():
            result = await db.execute(delete(Notification).where(Notification.id == notification_id))
            await db.commit()
            return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Повідомлення з помилкою {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
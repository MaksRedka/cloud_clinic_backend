from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from fastapi import HTTPException, status
from .models import User

# Create
async def create_user(db: AsyncSession, user_uuid: str, user_type: str, name: str, email: str, password: str, data: dict):
    try:
        db_user = User(user_uuid=user_uuid, user_type=user_type, name=name, email=email, password=password, data=data)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error creating user {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Read
async def get_user(db: AsyncSession, user_uuid: str):
    result = await db.execute(select(User).filter(User.user_uuid == user_uuid))
    return result.scalar()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Update
async def update_user(db: AsyncSession, user_uuid: str, data: dict):
    try:
        result = await db.execute(update(User).where(User.user_uuid == user_uuid).values(data))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error updating user {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Delete
async def delete_user(db: AsyncSession, user_uuid: str):
    try:
        result = await db.execute(delete(User).where(User.user_uuid == user_uuid))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error deleting user {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

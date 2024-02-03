from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from fastapi import HTTPException, status
from src.treatment_plans.models import TreatmentPlan

# Create
async def create_treatment_plan(db: AsyncSession, user_uuid: str, title: str, description: str, is_open: bool, data: dict):
    try:
        db_plan = TreatmentPlan(user_uuid=user_uuid, title=title, description=description, is_open=is_open, data=data)
        db.add(db_plan)
        await db.commit()
        await db.refresh(db_plan)
        return db_plan
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error creating treatment plan {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Read
async def get_treatment_plan(db: AsyncSession, plan_id: int):
    result = await db.execute(select(TreatmentPlan).filter(TreatmentPlan.id == plan_id))
    return result.scalar()

async def get_all_treatment_plans(db: AsyncSession):
    result = await db.execute(select(TreatmentPlan))
    return result.scalars().all()

# Update
async def update_treatment_plan(db: AsyncSession, plan_id: int, data: dict):
    try:
        result = await db.execute(update(TreatmentPlan).where(TreatmentPlan.id == plan_id).values(data))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error updating treatment plan {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

# Delete
async def delete_treatment_plan(db: AsyncSession, plan_id: int):
    try:
        result = await db.execute(delete(TreatmentPlan).where(TreatmentPlan.id == plan_id))
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            detail={"message": f"Error deleting treatment plan {e}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

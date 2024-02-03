from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.chat.models import *
from src.notification.models import Notification
from src.treatment_plans.models import TreatmentPlan
from src.user.models import User
from src.notification.schemas.models import NotificationCreate, NotificationUpdate, NotificationBase
from src.chat.schemas.models import ConversationCreate, ConversationUpdate, MessageCreate, MessageUpdate, MessagenBase, ConversationBase
from src.treatment_plans.schemas.models import TreatmentPlanCreate, TreatmentPlanUpdate, TreatmentPlanBase
from src.user.schemas.models import UserCreate, UserUpdate, UserBase
from src.chat.crud import (
    create_conversation, get_conversation, get_all_conversations,
    update_conversation, delete_conversation,
    create_message, get_message, get_all_messages,
    update_message, delete_message
)
from src.notification.crud import (
    create_notification, get_notification, get_all_notifications,
    update_notification, delete_notification) 
from src.treatment_plans.crud import (
    create_treatment_plan, get_treatment_plan, get_all_treatment_plans,
    update_treatment_plan, delete_treatment_plan
)
from src.user.crud import (
    create_user, get_user, get_all_users,
    update_user, delete_user,
)
from typing import List

from src.database import get_postgres

router = APIRouter()

# Conversation routes

@router.post("/conversation/", response_model=ConversationBase)
async def create_conversation_route(
    data: ConversationCreate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await create_conversation(db, **data.model_dump())
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
                        
@router.get("/conversation/{chat_uuid}", response_model=ConversationBase)
async def get_conversation_route(chat_uuid: str, db: AsyncSession = Depends(get_postgres)):
    payload = await get_conversation(db, chat_uuid)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)

@router.get("/conversation/", response_model=List[ConversationBase])
async def get_all_conversations_route(db: AsyncSession = Depends(get_postgres)):
    payload = await get_all_conversations(db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.put("/conversation/{chat_uuid}", response_model=ConversationBase)
async def update_conversation_route(
    chat_uuid: str,
    data: ConversationUpdate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await update_conversation(db, chat_uuid, data.model_dump(exclude_unset=True))
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.delete("/conversation/{chat_uuid}", response_model=ConversationBase)
async def delete_conversation_route(chat_uuid: str, db: AsyncSession = Depends(get_postgres)):
    payload = await delete_conversation(db, chat_uuid)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
# Message routes

@router.post("/message/", response_model=MessagenBase)
async def create_message_route(
    data: MessageCreate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await create_message(db, **data.model_dump())
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/message/{message_id}", response_model=MessagenBase)
async def get_message_route(message_id: int, db: AsyncSession = Depends(get_postgres)):
    payload = await get_message(db, message_id)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/message/", response_model=List[MessagenBase])
async def get_all_messages_route(db: AsyncSession = Depends(get_postgres)):
    payload = await get_all_messages(db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.put("/message/{message_id}", response_model=MessagenBase)
async def update_message_route(
    message_id: int,
    data: MessageUpdate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await update_message(db, message_id, data.model_dump(exclude_unset=True))
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.delete("/message/{message_id}", response_model=MessagenBase)
async def delete_message_route(message_id: int, db: AsyncSession = Depends(get_postgres)):
    payload = await delete_message(db, message_id)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
# Treatment Plan routes

@router.post("/treatment-plan/", response_model=TreatmentPlanBase)
async def create_treatment_plan_route(
    data: TreatmentPlanCreate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await create_treatment_plan(db, **data.model_dump())
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/treatment-plan/{plan_id}", response_model=TreatmentPlanBase)
async def get_treatment_plan_route(plan_id: int, db: AsyncSession = Depends(get_postgres)):
    payload = await get_treatment_plan(db, plan_id)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/treatment-plan/", response_model=List[TreatmentPlanBase])
async def get_all_treatment_plans_route(db: AsyncSession = Depends(get_postgres)):
    payload = await get_all_treatment_plans(db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.put("/treatment-plan/{plan_id}", response_model=TreatmentPlanBase)
async def update_treatment_plan_route(
    plan_id: int,
    data: TreatmentPlanUpdate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await update_treatment_plan(db, plan_id, data.model_dump(exclude_unset=True))
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.delete("/treatment-plan/{plan_id}", response_model=TreatmentPlanBase)
async def delete_treatment_plan_route(plan_id: int, db: AsyncSession = Depends(get_postgres)):
    payload = await delete_treatment_plan(db, plan_id)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
# User routes

@router.post("/user/", response_model=UserBase)
async def create_user_route(
    data: UserCreate,
    db: AsyncSession = Depends(get_postgres)
)-> JSONResponse:
    payload = await create_user(db, **data.model_dump())
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK
)

@router.get("/user/{user_uuid}", response_model=UserBase)
async def get_user_route(user_uuid: str, db: AsyncSession = Depends(get_postgres)):
    payload = await get_user(db, user_uuid)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/user/", response_model=List[UserBase])
async def get_all_users_route(db: AsyncSession = Depends(get_postgres)):
    payload = await get_all_users(db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.put("/user/{user_uuid}", response_model=UserBase)
async def update_user_route(
    user_uuid: str,
    data: UserUpdate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await update_user(db, user_uuid, data.model_dump(exclude_unset=True))
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.delete("/user/{user_uuid}")
async def delete_user_route(user_uuid: str, db: AsyncSession = Depends(get_postgres)):
    payload = await delete_user(db, user_uuid)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)

@router.post("/notification/", response_model=NotificationBase)
async def create_notification_route(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await create_notification(db, **data.model_dump())
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/notification/{notification_id}", response_model=NotificationBase)
async def get_notification_route(notification_id: int, db: AsyncSession = Depends(get_postgres)):
    payload = await get_notification(db, notification_id)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.get("/notification/", response_model=List[NotificationBase])
async def get_all_notifications_route(db: AsyncSession = Depends(get_postgres)):
    payload = await get_all_notifications(db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.put("/notification/{notification_id}", response_model=NotificationBase)
async def update_notification_route(
    notification_id: int,
    data: NotificationUpdate,
    db: AsyncSession = Depends(get_postgres)
):
    payload = await update_notification(db, notification_id, data.model_dump(exclude_unset=True))
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
    
@router.delete("/notification/{notification_id}", response_model=NotificationBase)
async def delete_notification_route(notification_id: int, db: AsyncSession = Depends(get_postgres)):
    payload = await delete_notification(db, notification_id)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)
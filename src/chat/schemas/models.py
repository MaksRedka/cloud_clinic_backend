"""Schemas to represent languages application models."""

from pydantic import BaseModel, Json


class ConversationBase(BaseModel):
    chat_uuid: str
    user_uuid: str
    doctor_uuid: str
    data: Json

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    data: Json
# Message schemas

class MessagenBase(BaseModel):
    chat_uuid: str
    data: Json
    
class MessageCreate(MessagenBase):
    pass

class MessageUpdate(BaseModel):
    data: Json
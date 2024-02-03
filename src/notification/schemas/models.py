"""Schemas to represent languages application models."""

from pydantic import BaseModel, Json


class NotificationBase(BaseModel):
    message: str
    type: str
    data: Json

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    data: Json
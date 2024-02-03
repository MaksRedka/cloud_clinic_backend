"""Schemas to represent languages application models."""

from pydantic import BaseModel, Json

# User schemas

class UserBase(BaseModel):
    user_uuid: str
    user_type: str
    name: str
    email: str
    password: str
    data: Json

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str
    data: Json
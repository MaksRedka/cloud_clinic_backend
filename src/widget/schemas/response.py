"""Response schemas for chat application."""
from pydantic import BaseModel
from enum import Enum

from src.widget.schemas.models import MessageTypeEnum


class ResponseBase(BaseModel):
    """Schema to represent response for chatbot client side."""
    return_type: MessageTypeEnum
    payload: str


class ResponseNewBase(BaseModel):
    """Schema to represent response for new api protocol."""
    return_type: str
    return_data: str
    customizing: dict

class ResponseTypeEnum(str, Enum):
    """Enum to represent response type"""
    GREETING = "greeting"
    ANSWER = "answer"
    STOP = "stop"
    CONFIRM = "confirm"
    FEEDBACK = "feedback"
    SAVING = "saving"

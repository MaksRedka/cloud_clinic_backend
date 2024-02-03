"""Schemas for models in chat application."""
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from src.widget.schemas.request import QueryTypeEnum


class MessageTypeEnum(str, Enum):
    """Enum to represent message_type in MessageCreate."""
    GREETING = "greeting"
    QUESTION = "question"
    ANSWER = "answer"
    MESSAGE = "message"
    TERMINATING = "terminating"
    RATING = "rating"
    FINISH = "finish"
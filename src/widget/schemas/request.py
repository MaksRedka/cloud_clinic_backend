"""Request schemas for chat application."""
from enum import Enum
from uuid import UUID

import pydantic
from pydantic import BaseModel


class QueryTypeEnum(str, Enum):
    """Enum for representation request events."""
    START = "start"
    """Chat creation. Retrieving greeting messages."""
    QUESTION = "question"
    """Chat continuation. Retrieving answer messages."""
    HISTORY = "history"
    """Restore chat history. Retrieving chat history."""
    TIMEOUT = "timeout"
    """Timeout signal."""
    RESTART = "restart"
    """Restart event."""
    RATING = "rating"
    """Rate user experience."""


class RequestBase(BaseModel):
    """Schema to represent request from client side."""
    product_id: UUID
    session_id: UUID
    query_type: QueryTypeEnum
    payload: None | str | int

    @pydantic.root_validator(pre=True)
    def validate_payload(cls, fields):
        """Validate request body for event_types that must have payload value None."""
        events: list[str] = [QueryTypeEnum.START.value, QueryTypeEnum.HISTORY.value,
                             QueryTypeEnum.RESTART.value, QueryTypeEnum.TIMEOUT.value, ]
        for event in events:
            if fields["query_type"] == event and fields['payload'] is not None:
                raise ValueError(f"Request with event_type {event} should have payload value null.")
        return fields

    @pydantic.root_validator(pre=True)
    def validate_payload_for_event_type_question(cls, fields):
        """
        Validate request body for event_type QUESTION.
        Payload must be a string with question.
        """
        if fields["query_type"] == QueryTypeEnum.QUESTION.value and not isinstance(fields['payload'], str):
            raise ValueError("Request with event_type 'question' must have payload value string.")
        return fields

    @pydantic.root_validator(pre=True)
    def validate_payload_for_event_type_rating(cls, fields):
        """
        Validate request body for event_type RATING.
        Payload must be None or integer in range from 1 to 5.
        """
        if fields["query_type"] == QueryTypeEnum.RATING.value:
            if fields["payload"] is not None:
                if fields["payload"] not in range(1, 6):
                    raise ValueError(
                        "Request with event_type 'rating' should have payload value null or integer in range from 1 to 5.")
        return fields


class VerifyProductUUIDRequest(BaseModel):
    """Request to verify product availability."""
    uuid: UUID


class VerifyProductSlugRequest(BaseModel):
    """Request to verify product availability."""
    host: str
    path: str


class QueryTypeNewEnum(str, Enum):
    """Enum represents query types for new api protocol."""
    START = "start"
    QUESTION = "question"
    RESTART = "restart"
    FINISH = "finish"
    FEEDBACK = "feedback"


class RequestNewBase(BaseModel):
    """Schema to represent request for new protocol."""
    product_id: UUID
    session_id: UUID
    agent_lang: str
    query_type: QueryTypeNewEnum
    query_data: str | None | int

    @pydantic.model_validator(mode="before")
    def validate_query_data_for_start(cls, fields):
        if fields["query_type"] == QueryTypeNewEnum.START.value and \
                fields['query_data'] is not None:
            raise ValueError()
        return fields

    @pydantic.model_validator(mode="before")
    def validate_query_data_for_question(cls, fields):
        if fields["query_type"] == QueryTypeNewEnum.QUESTION.value and not \
                isinstance(fields['query_data'], str):
            raise ValueError()
        return fields

    @pydantic.model_validator(mode="before")
    def validate_query_data_for_restart(cls, fields):
        if fields["query_type"] == QueryTypeNewEnum.RESTART.value and \
                fields['query_data'] is not None:
            raise ValueError()
        return fields

    @pydantic.model_validator(mode="before")
    def validate_query_data_for_feedback(cls, fields):
        if fields["query_type"] == QueryTypeNewEnum.FEEDBACK.value:
            if fields["query_data"] is not None:
                if fields["query_data"] not in range(1, 6):
                    raise ValueError()
        return fields

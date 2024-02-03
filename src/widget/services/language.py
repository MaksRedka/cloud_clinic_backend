"""Services to manage localization functionality for pipeline."""
import re

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.languages.utils.utils import convert_language_to_base, retrive_default_language_data
from src.widget.schemas.response import ResponseNewBase, ResponseTypeEnum


def _get_code_from_string(string: str) -> str:
    """Get first letters from string till first no-letter symbol."""
    pattern: str = r'^[A-Za-z]+'
    match = re.search(pattern, string)

    extracted_code: str = match.group()
    return extracted_code

async def get_language_for_widget_start(db: AsyncSession, agent_lang: str) -> ResponseNewBase:
    language = await retrive_default_language_data()
    converted_language = await convert_language_to_base(language)

    return ResponseNewBase(return_type=ResponseTypeEnum.GREETING.value,
                                   return_data=converted_language.greeting_text,
                                   customizing=converted_language.get_widget_repr())

async def get_response_for_widget_question(
        db: AsyncSession) -> ResponseNewBase:
    """Return response for widget question query."""
    language = await retrive_default_language_data()
    converted_language = await convert_language_to_base(language)

    return ResponseNewBase(return_type=ResponseTypeEnum.ANSWER.value,
                           return_data="",
                           customizing=converted_language.get_widget_repr())


async def get_response_for_widget_restart(
        db: AsyncSession) -> ResponseNewBase:
    """Return response for widget restart query."""
    language = await retrive_default_language_data()
    converted_language = await convert_language_to_base(language)

    return ResponseNewBase(return_type=ResponseTypeEnum.CONFIRM.value,
                           return_data=converted_language.restart_text,
                           customizing=converted_language.get_widget_repr())


async def get_response_for_widget_finish(
        db: AsyncSession) -> ResponseNewBase:
    """Return response for widget finish query."""
    language = await retrive_default_language_data()
    converted_language = await convert_language_to_base(language)

    return ResponseNewBase(return_type=ResponseTypeEnum.FEEDBACK.value,
                           return_data=converted_language.feedback_text,
                           customizing=converted_language.get_widget_repr())


async def get_get_response_for_widget_feedback(
        db: AsyncSession) -> ResponseNewBase:
    """Return response for widget feedback query."""
    language = await retrive_default_language_data()
    converted_language = await convert_language_to_base(language)

    return ResponseNewBase(return_type=ResponseTypeEnum.SAVING.value,
                           return_data="not implemented",
                           customizing=converted_language.get_widget_repr())

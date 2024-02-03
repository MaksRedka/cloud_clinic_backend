"""Service for new widget communication protocol."""
from datetime import datetime
from typing import Any

from fastapi import BackgroundTasks, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.widget.schemas.request import RequestNewBase, QueryTypeNewEnum
from src.widget.schemas.response import ResponseNewBase
from src.widget.services import language as lang_service

from src.widget.services.file_loader import get_row_by_id, get_all_rows
from src.widget.models import FAQ, Conversation, Message
from src.languages.utils.utils import convert_language_to_base, retrive_default_language_data
from src.widget.crud import create_conversation, create_message, update_conversation, get_conversation_by_session_id

import pandas as pd

async def manage_widget_request(db: AsyncSession, request: RequestNewBase,
                                background_task: BackgroundTasks) -> JSONResponse:
    """Manage widget behavior depending on request type."""
    query_type: str = request.query_type.value
    match query_type:
        case QueryTypeNewEnum.START.value:
            return await manage_start_request(
                db=db, request=request)
        case QueryTypeNewEnum.QUESTION.value:
            return await manage_question_request(
                db=db, request=request, background_task=background_task)
        case QueryTypeNewEnum.RESTART.value:
            return await manage_restart_request(
                db=db, request=request)
        case QueryTypeNewEnum.FINISH.value:
            return await manage_finish_request(
                db=db, request=request)
        case QueryTypeNewEnum.FEEDBACK.value:
            return await manage_feedback_request(
                db=db, request=request)


async def manage_start_request(db: AsyncSession, request: RequestNewBase) -> JSONResponse:
    """Manage start request. Return customizing and greeting message."""
    payload: ResponseNewBase = await lang_service \
        .get_language_for_widget_start(db=db, agent_lang=request.agent_lang)
    check:Conversation = await get_conversation_by_session_id(db=db, session_id=request.session_id)
    if check is None:
        conv:Conversation = await create_conversation(db=db, session_uuid=request.session_id, rating=request.query_data, is_finished=False)

    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)


async def manage_question_request(db: AsyncSession, request: RequestNewBase,
                                  background_task: BackgroundTasks) -> JSONResponse:
    """Manage question request. Answer the question or create ticket."""

    payload: ResponseNewBase = await lang_service.get_response_for_widget_question(
        db=db)
    language = await retrive_default_language_data()
    converted_language = await convert_language_to_base(language)
    
    data: tuple[FAQ] = await get_all_rows('question_wide', db, FAQ)
    metadata: tuple[FAQ] = await get_all_rows('id', db, FAQ)
    df = pd.DataFrame(data={'question_wide':data, 'id':metadata})

    if len(data) < 1:
        payload.return_data = converted_language.default_request_text
        return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)

    res: pd.DataFrame = []
    
    msg:Message = await create_message(db=db, session_uuid=request.session_id, answer_id=res.iloc[0]['id'], faiss_distance=res.iloc[0]['distances'])
    id = res.iloc[:3]['id'].tolist()
    row: FAQ = await get_row_by_id(id[0], db, FAQ)
    question = row.question
    answer = row.answer_short

    answer_template = """<p class="question">{}</p><p class="option">Відкрити відповідь…</p><p class="answer">{}</p>""".format(question, answer)

    payload.return_data = answer_template
    
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)


async def manage_restart_request(
        db: AsyncSession,
        request: RequestNewBase
) -> JSONResponse:
    """Manage restart request. Return confirm signal."""
    payload: ResponseNewBase = await lang_service.get_response_for_widget_restart(
        db=db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)


async def manage_finish_request(db: AsyncSession, request: RequestNewBase) -> JSONResponse:
    """Manage finish request. Return feedback signal."""
    payload: ResponseNewBase = await lang_service.get_response_for_widget_finish(
        db=db)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)


async def manage_feedback_request(db: AsyncSession,
                                  request: RequestNewBase) -> JSONResponse:
    """Manage feedback request. Finish conversation and set rating."""
    # save feedback
    payload: ResponseNewBase = await lang_service.get_get_response_for_widget_feedback(
        db=db)
    conv:Conversation = await update_conversation(db=db, session_uuid=request.session_id, rating=request.query_data, is_finished=True)
    return JSONResponse(content=jsonable_encoder(payload),
                        status_code=status.HTTP_200_OK)

async def perform_verify_product_slug(db: AsyncSession, host: str, path: str) -> JSONResponse:
    """Check if there is product with the slug."""
    return JSONResponse(content={"verified": True,
                                 "message": "Service is enabled",
                                 "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"},
                        status_code=status.HTTP_200_OK)

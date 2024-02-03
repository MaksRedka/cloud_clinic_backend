from fastapi import UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import types, select, text
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.widget.models import FAQ
import io
import os



async def faiss_create(db: AsyncSession):
    data: tuple[str] = await get_all_rows('question_wide', db, FAQ)
    metadata: tuple[str] = await get_all_rows('id', db, FAQ)
    df = pd.DataFrame(data={'question_wide':data, 'id':metadata})

async def xlxs_to_df(file: UploadFile|io.BufferedReader, columns: list[str]=None) -> pd.DataFrame:
    if isinstance(file, io.BufferedReader):
        content = file.read()
    else:
        content = await file.read()

    xl = pd.ExcelFile(io.BytesIO(content))
    # Load a sheet into a DataFrame by its name
    df: pd.DataFrame = xl.parse()
    df['id'] = df.index
    if columns:
        df = df[columns]
    return df

async def upload_file(file: UploadFile, db: AsyncSession, tablename: str, columns: list[str]=None) -> JSONResponse:
    # Load spreadsheet
    df = await xlxs_to_df(file=file, columns=columns)
    sql_types = {'id': types.INTEGER}

    # Write records stored in a DataFrame to a SQL database.
    conn = await db.connection()
    try:
        await conn.run_sync(lambda sync_conn: df.to_sql(tablename, sync_conn, if_exists='replace', index=False, dtype=sql_types, method='multi', chunksize=50))
        await db.commit()
    except Exception as er:
        await db.rollback()
        raise HTTPException(
            detail={"message": "Something went wrong! {}".format(er)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return JSONResponse(content={"message": "File uploaded"},
                        status_code=200)

async def get_all_rows(column_name:str, db: AsyncSession, obj: object) -> tuple[object]:
    rows: tuple[object] = await db.execute(select(getattr(obj, column_name)).order_by(obj.id))
    return rows.scalars().all()
    
async def get_row_by_id(id: int, db: AsyncSession, obj:object) -> object:
    # Connect to the database
    answers: tuple[object] = await db.execute(select(obj).filter(obj.id == id))
    return answers.scalars().first()


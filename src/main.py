from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.widget.router import router as widget_router
from src.database import initialize_postgres
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_postgres()
    yield
    

app = FastAPI(lifespan=lifespan)

origins = ["*", ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(widget_router)

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.leaderboard import router as leaderboard_router
from app.core.database import connect, close, ensure_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize DB client and create indexes
    connect()
    await ensure_indexes()
    try:
        yield
    finally:
        close()


app = FastAPI(lifespan=lifespan)


app.include_router(leaderboard_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
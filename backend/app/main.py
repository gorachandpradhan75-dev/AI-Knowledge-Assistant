from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.api.documents import router as document_router
from app.core.security import create_access_token
from app.db.mongodb import (
    connect_to_mongo,
    close_mongo_connection,
    get_database,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

# Authentication routes
app.include_router(auth_router)
app.include_router(document_router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "status": "running",
    }


@app.get("/health/db")
async def db_health():
    db = get_database()
    result = await db.command("ping")
    return {"mongo": result}


@app.get("/token-test")
async def token_test():
    token = create_access_token("gorac")
    return {"token": token}
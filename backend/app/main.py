from contextlib import asynccontextmanager
from app.api.voice import router as voice_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.api.documents import router as document_router
from app.api.resume import router as resume_router
from app.api.translation import router as translation_router
from app.core.security import create_access_token
from app.api.dashboard import (
    router as dashboard_router,
)
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Authentication routes
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(resume_router)
app.include_router(translation_router)
app.include_router(voice_router)
app.include_router(dashboard_router)
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
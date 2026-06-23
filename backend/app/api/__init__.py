from fastapi import APIRouter, HTTPException, status

from app.db.mongodb import get_database
from app.models.user import new_user_document
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    TokenResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    db = get_database()

    existing_email = await db.users.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    existing_username = await db.users.find_one(
        {"username": user.username}
    )
    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    user_doc = new_user_document(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
    )

    await db.users.insert_one(user_doc)

    return {
        "message": "User registered successfully"
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(credentials: UserLogin):
    db = get_database()

    user = await db.users.find_one(
        {"email": credentials.email}
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        credentials.password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        str(user["_id"])
    )

    refresh_token = create_refresh_token(
        str(user["_id"])
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )
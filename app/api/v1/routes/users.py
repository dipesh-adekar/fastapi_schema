from typing import Annotated

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.v1.schemas.user import PaginatedUserResponseV1
from app.db.mongo_db import get_mongodb
from app.schemas.user import Token, UserCreate, UserLogin
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
        429: {"description": "Too Many Requests"},
    },
)


@router.post("/register")
async def register_user_v1(
    user_create: UserCreate,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_mongodb)],
):
    user_service = UserService(db)
    await user_service.create_user(user_create)
    return {"message": "User registered"}


@router.post("/login", response_model=Token)
async def login_v1(
    user_login: UserLogin,
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
    # _=Depends(rate_limiter),
):
    """Login user and get access token (API v1)."""
    user_service = UserService(db)
    access_token = await user_service.authenticate_user(
        user_login.username, user_login.password
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=PaginatedUserResponseV1)
async def list_users_v1(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    active_only: bool = Query(True, description="Filter active users only"),
    db: AsyncIOMotorDatabase = Depends(get_mongodb),
):
    """List users with pagination (API v1)."""
    user_service = UserService(db)
    users = await user_service.list_users(skip, limit, active_only)

    # Simple pagination for v1
    return PaginatedUserResponseV1(
        data=users,
        pagination={"skip": skip, "limit": limit, "has_more": len(users) == limit},
    )

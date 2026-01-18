from typing import Annotated, Any

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase  # type: ignore

from app.db.mongo_db import get_mongodb  # type: ignore
from app.services.user_service import UserService
from app.schemas.user import UserCreate

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
    db: Annotated[AsyncIOMotorDatabase[Any], Depends(get_mongodb)],  # type: ignore
):
    user_service = UserService(db)  # type: ignore
    await user_service.create_user(user_create)
    return {"message": "User registered"}

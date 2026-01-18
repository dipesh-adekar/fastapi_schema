from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase  # type: ignore

from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncIOMotorDatabase[Any]) -> None:  # type: ignore
        self.db: Any = db  # type: ignore
        # Get collection name from User model config
        # Access Config class attribute to avoid type expression issues
        user_config = User.Config
        collection_name: str = user_config.collection
        self.collection = db[collection_name]  # type: ignore

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID with caching."""
        user_data: Any = await self.collection.find_one({"_id": ObjectId(user_id)})  # type: ignore
        if user_data:
            return User(**user_data)  # type: ignore
        return None

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""

        user_dict = user_create.model_dump(exclude={"password"})
        user_dict["hashed_password"] = user_create.password
        user_dict["created_at"] = datetime.now(UTC)
        user_dict["updated_at"] = datetime.now(UTC)
        result: Any = await self.collection.insert_one(user_dict)  # type: ignore

        user = await self.get_user_by_id(str(result.inserted_id))  # type: ignore
        if user is None:
            raise ValueError("Failed to create user")
        return user

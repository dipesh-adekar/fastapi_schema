from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.v1.schemas.user import UserResponse
from app.core.cache import cache_response
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db[User.Config.collection]

    @cache_response(ttl=60, key_prefix="user")
    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID with caching."""
        user_data: Any = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(**user_data)
        return None

    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username with caching."""
        user_data: Any = await self.collection.find_one({"username": username})
        if user_data:
            return User(**user_data)
        return None

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""

        hashed_password = get_password_hash(user_create.password)
        user_dict = user_create.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        user_dict["created_at"] = datetime.now(UTC)
        user_dict["updated_at"] = datetime.now(UTC)
        result: Any = await self.collection.insert_one(user_dict)

        from app.db.redis import RedisManager

        cache_backend = await RedisManager.get_cache_backend()
        await cache_backend.delete_pattern("user*")

        user = await self.get_user_by_id(str(result.inserted_id))
        if user is None:
            raise ValueError("Failed to create user")
        return user

    async def authenticate_user(self, username: str, password: str) -> str | None:
        """Authenticate user."""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        # Update last login
        await self.collection.update_one(
            {"_id": user.id}, {"$set": {"last_login": datetime.now(UTC)}}
        )

        return create_access_token(subject=str(user.id))

    @cache_response(ttl=60, key_prefix="users_list")
    async def list_users(
        self, skip: int = 0, limit: int = 100, active_only: bool = False
    ) -> list[UserResponse]:
        """List users with pagination and caching."""
        # Build query dict - create a fresh dict each time
        query: dict[str, Any] = {}
        if active_only:
            query["is_active"] = True
        cursor = self.collection.find(query).skip(skip).limit(limit)
        users = []
        async for user_data in cursor:
            user = User(**user_data)
            user_dict = user.model_dump(mode="json")
            users.append(UserResponse(**user_dict))

        return users

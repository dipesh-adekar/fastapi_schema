from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase  # type: ignore

from config import config


class MongoDB:
    _client: AsyncIOMotorClient[Any] | None = None  # type: ignore[assignment]
    _database: AsyncIOMotorDatabase[Any] | None = None  # type: ignore[assignment]

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient[Any]:  # type: ignore
        """Get MongoDB client with connection pooling."""
        if cls._client is None:  # type: ignore
            cls._client = AsyncIOMotorClient(  # type: ignore
                config.MONGO_URL,
                maxPoolSize=config.MONGO_MAX_POOL_SIZE,
                minPoolSize=config.MONGO_MIN_POOL_SIZE,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=30000,
                retryWrites=True,
                retryReads=True,
            )

            # Test connection
            try:
                if cls._client is not None:  # type: ignore
                    await cls._client.admin.command("ping")  # type: ignore
                    print("✅ MongoDB connected successfully")
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                raise

        return cls._client  # type: ignore

    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase[Any]:  # type: ignore
        """Get database instance."""
        if cls._database is None:  # type: ignore
            client: Any = await cls.get_client()  # type: ignore
            cls._database = client[config.MONGO_DB_NAME]  # type: ignore

        return cls._database  # type: ignore

    @classmethod
    async def close(cls) -> None:
        """Close MongoDB connection."""
        if cls._client:  # type: ignore
            cls._client.close()  # type: ignore
            cls._client = None
            cls._database = None

    @classmethod
    async def get_collection(cls, collection_name: str) -> Any:
        """Get collection from database."""
        db: Any = await cls.get_database()  # type: ignore
        return db[collection_name]  # type: ignore


# Dependency for FastAPI
async def get_mongodb() -> AsyncIOMotorDatabase[Any]:  # type: ignore
    """Dependency to get MongoDB database instance."""
    return await MongoDB.get_database()  # type: ignore

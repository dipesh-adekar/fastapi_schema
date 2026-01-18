from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import config


class MongoDB:
    _client: Any | None = None
    _database: Any | None = None

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        """Get MongoDB client with connection pooling."""
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
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
                if cls._client is not None:
                    await cls._client.admin.command("ping")
                    print("✅ MongoDB connected successfully")
            except Exception as e:
                print(f"❌ MongoDB connection failed: {e}")
                raise

        return cls._client

    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if cls._database is None:
            client: Any = await cls.get_client()
            cls._database = client[config.MONGO_DB_NAME]

        return cls._database

    @classmethod
    async def close(cls) -> None:
        """Close MongoDB connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._database = None

    @classmethod
    async def get_collection(cls, collection_name: str) -> Any:
        """Get collection from database."""
        db: Any = await cls.get_database()
        return db[collection_name]


# Dependency for FastAPI
async def get_mongodb() -> AsyncIOMotorDatabase:
    """Dependency to get MongoDB database instance."""
    return await MongoDB.get_database()

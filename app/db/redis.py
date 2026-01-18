import redis.asyncio as redis
from redis.asyncio import ConnectionPool

from app.core.cache import CacheBackend
from config import config


class RedisManager:
    _pool: ConnectionPool | None = None
    _cache_backend: CacheBackend | None = None

    @classmethod
    def get_pool(cls) -> ConnectionPool:
        """Get Redis connection pool."""
        if cls._pool is None:
            cls._pool = ConnectionPool.from_url(
                config.REDIS_URL,
                max_connections=config.REDIS_POOL_SIZE,
                decode_responses=False,
                socket_connect_timeout=5,
                socket_keepalive=True,
            )
        return cls._pool

    @classmethod
    async def get_client(cls) -> redis.Redis:
        """Get Redis client from pool."""
        pool = cls.get_pool()
        return redis.Redis(connection_pool=pool)

    @classmethod
    async def get_cache_backend(cls) -> CacheBackend:
        """Get cache backend instance."""
        if cls._cache_backend is None:
            client = await cls.get_client()
            cls._cache_backend = CacheBackend(client)
        return cls._cache_backend

    @classmethod
    async def close(cls):
        """Close Redis connections."""
        if cls._pool:
            await cls._pool.disconnect()
            cls._pool = None
            # cls._cache_backend = None

    @classmethod
    async def ping(cls) -> bool:
        """Check Redis connection."""
        try:
            client = await cls.get_client()
            await client.ping()
            return True
        except Exception:
            return False


# Dependency for FastAPI
async def get_redis() -> redis.Redis:
    """Dependency to get Redis client."""
    return await RedisManager.get_client()


async def get_cache_backend() -> CacheBackend:
    """Dependency to get cache backend."""
    return await RedisManager.get_cache_backend()

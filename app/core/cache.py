import asyncio
import hashlib
import inspect
import redis
import pickle
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional, Union

from config import config


class CacheBackend:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            data = await self.redis.get(key)
            if data:
                return pickle.loads(data)
        except Exception:
            return None
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        try:
            ttl = ttl or config.CACHE_TTL
            await self.redis.setex(key, ttl, pickle.dumps(value))
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            await self.redis.delete(key)
            return True
        except Exception:
            return False

    async def delete_pattern(self, pattern: str) -> bool:
        """Delete keys matching pattern."""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
            return True
        except Exception:
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            return await self.redis.exists(key) > 0
        except Exception:
            return False


def cache_key_builder(func: Callable, *args, **kwargs) -> str:
    """Build cache key from function and arguments."""
    # Create a hash of function name and arguments
    key_parts = [func.__module__, func.__name__]

    # Check if this is an instance method (has 'self' as first arg)
    # Skip the first argument (self) for instance methods
    sig = inspect.signature(func)
    is_method = len(sig.parameters) > 0 and list(sig.parameters.keys())[0] == "self"

    # Add args, skipping 'self' for instance methods
    args_to_include = args[1:] if is_method and len(args) > 0 else args
    for arg in args_to_include:
        key_parts.append(str(arg))

    # Add kwargs
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")

    # Create hash
    key_string = ":".join(key_parts)
    print(f"Key string: {key_string}")
    return hashlib.md5(key_string.encode()).hexdigest()


def cache_response(
    ttl: Optional[int] = None,
    key_prefix: str = "cache",
    exclude_args: Optional[list] = None,
):
    """
    Decorator for caching function responses.

    Args:
        ttl: Cache TTL in seconds
        key_prefix: Prefix for cache key
        exclude_args: List of argument names to exclude from cache key
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not config.CACHE_ENABLED:
                return await func(*args, **kwargs)

            # Filter out excluded args from kwargs for cache key
            cache_kwargs = kwargs.copy()
            if exclude_args:
                for arg_name in exclude_args:
                    cache_kwargs.pop(arg_name, None)

            cache_key = f"{key_prefix}:{cache_key_builder(func, *args, **cache_kwargs)}"
            print(f"Cache key: {cache_key}")

            # Try to get from cache
            from app.db.redis import get_cache_backend

            cache: CacheBackend = await get_cache_backend()

            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl or config.CACHE_TTL)

            return result

        return wrapper

    return decorator

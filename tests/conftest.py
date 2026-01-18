import asyncio
import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


from app.db.mongo_db import get_mongodb  # noqa: E402
from config import config  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def mongodb() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    client: Any = AsyncIOMotorClient(config.MONGO_URL)
    db: Any = client[config.MONGO_DB_NAME]
    yield db
    try:
        collections: Any = await db.list_collection_names()
        for collection_name in collections:
            await db.drop_collection(collection_name)
    except Exception:
        pass
    finally:
        client.close()


@pytest_asyncio.fixture
async def async_client(
    mongodb: AsyncIOMotorDatabase,
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_mongodb() -> AsyncIOMotorDatabase:
        return mongodb

    app.dependency_overrides[get_mongodb] = override_get_mongodb
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

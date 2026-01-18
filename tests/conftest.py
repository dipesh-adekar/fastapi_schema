import pytest
import pytest_asyncio
import asyncio
import sys
from typing import Any, AsyncGenerator
from pathlib import Path
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase  # type: ignore


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


from main import app  # noqa: E402
from config import config  # noqa: E402
from app.db.mongo_db import get_mongodb  # noqa: E402  # type: ignore


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def mongodb() -> AsyncGenerator[AsyncIOMotorDatabase[Any], None]:  # type: ignore
    client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(config.MONGO_URL)  # type: ignore
    db: AsyncIOMotorDatabase[Any] = client[config.MONGO_DB_NAME]  # type: ignore
    yield db
    try:
        collections: Any = await db.list_collection_names()  # type: ignore
        for collection_name: Any in collections:  # type: ignore
            await db.drop_collection(collection_name)  # type: ignore
    except Exception:
        pass
    finally:
        client.close()  # type: ignore


@pytest_asyncio.fixture
async def async_client(mongodb: AsyncIOMotorDatabase[Any]) -> AsyncGenerator[AsyncClient, None]:  # type: ignore
    async def override_get_mongodb() -> AsyncIOMotorDatabase[Any]:  # type: ignore
        return mongodb  # type: ignore

    app.dependency_overrides[get_mongodb] = override_get_mongodb  # type: ignore
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

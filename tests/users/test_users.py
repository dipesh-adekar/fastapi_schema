from typing import Any

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase  # type: ignore

from config import config


@pytest.mark.asyncio
async def test_create_user(
    async_client: AsyncClient,
    mongodb: AsyncIOMotorDatabase[Any],  # type: ignore
) -> None:
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123",
        "full_name": "Test User",
    }

    response = await async_client.post(
        f"/api/v1/{config.SERVICE_NAME}/users/register", json=payload
    )

    assert response.status_code == 200
    user: Any = await mongodb["users"].find_one({"email": payload["email"]})  # type: ignore
    assert user is not None

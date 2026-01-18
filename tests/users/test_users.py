import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from config import config


class TestUserRegistrationFlow:
    """Test the complete user registration flow"""

    @pytest.mark.asyncio
    async def test_complete_registration_flow(
        self,
        async_client: AsyncClient,
        mongodb: AsyncIOMotorDatabase,
        # sample_user: dict,
    ) -> None:
        """Test registration -> login -> list users flow"""

        sample_user = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "secret123",
            "full_name": "Test User",
        }
        # Step 1: Register a new user
        register_response = await async_client.post(
            f"/api/v1/{config.SERVICE_NAME}/users/register",
            json=sample_user,
        )
        assert register_response.status_code == 200
        register_data = register_response.json()

        # Verify user data in response
        assert register_data["message"] == "User registered"

        # Verify user exists in database
        user = await mongodb["users"].find_one({"email": sample_user["email"]})
        assert user is not None
        assert user["username"] == sample_user["username"]

        # Step 2: Login with the registered user
        login_payload = {
            "username": sample_user["username"],
            "password": sample_user["password"],
        }
        login_response = await async_client.post(
            f"/api/v1/{config.SERVICE_NAME}/users/login",
            json=login_payload,
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

        access_token = token_data["access_token"]

        # Step 3: List users with authentication
        headers = {"Authorization": f"Bearer {access_token}"}
        list_response = await async_client.get(
            f"/api/v1/{config.SERVICE_NAME}/users/?active_only=False",
            headers=headers,
        )
        assert list_response.status_code == 200
        users = list_response.json()

        # Verify the registered user is in the list
        assert users["success"] is True
        assert len(users["data"]) >= 1
        user_emails = [user["email"] for user in users["data"]]
        assert sample_user["email"] in user_emails

from datetime import UTC, datetime
from typing import Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserResponse(BaseModel):
    """User response schema for API v1."""

    id: str = Field(alias="_id")
    username: str
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def convert_objectid_to_str(cls, v: Any) -> str:
        """Convert ObjectId to string if needed."""
        if isinstance(v, ObjectId):
            return str(v)
        return str(v)

    class Config:
        from_attributes = True
        populate_by_name = True


class PaginatedUserResponseV1(BaseModel):
    """Paginated user response for API v1."""

    success: bool = True
    data: list[UserResponse]
    pagination: dict | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

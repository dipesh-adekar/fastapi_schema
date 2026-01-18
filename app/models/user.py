from datetime import datetime
from enum import Enum
from typing import Optional

from app.models.base import BaseMongoModel


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"


class User(BaseMongoModel):
    username: str
    email: str
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    role: UserRole = UserRole.USER
    last_login: Optional[datetime] = None

    class Config:
        collection = "users"
        indexes = [
            {"key": [("email", 1)], "unique": True},
            {"key": [("username", 1)], "unique": True},
        ]

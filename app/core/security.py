import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from config import config


def _prepare_password_for_bcrypt(password: str) -> bytes:
    """
    Prepare password for bcrypt hashing.
    Bcrypt has a 72-byte limit, so we hash longer passwords with SHA-256 first.
    """
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        # Hash with SHA-256 first to get a fixed 32-byte hash
        return hashlib.sha256(password_bytes).digest()
    return password_bytes


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    Handles passwords longer than 72 bytes by hashing them first.
    """
    prepared_password = _prepare_password_for_bcrypt(password)
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prepared_password, salt)
    # Return as string (bcrypt hash is already encoded)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.
    """
    prepared_password = _prepare_password_for_bcrypt(plain_password)
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(prepared_password, hashed_bytes)


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a JWT access token.

    :param subject: user id (stored as `sub`)
    :param expires_delta: optional expiry override
    :param extra_claims: additional JWT claims
    """
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(UTC),
        "type": "access",
    }

    if extra_claims:
        payload.update(extra_claims)

    encoded_jwt = jwt.encode(
        payload,
        config.SECRET_KEY,
        algorithm=config.ALGORITHM,
    )
    return encoded_jwt

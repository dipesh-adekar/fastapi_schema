import os


class Config:
    SERVICE_NAME = "sample-app"

    MONGO_URL: str = os.getenv(
        "MONGO_URL",
        "mongodb://root:password@localhost:27017/fastapi_db?authSource=admin",
    )
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "fastapi_db")
    MONGO_MAX_POOL_SIZE: int = int(os.getenv("MONGO_MAX_POOL_SIZE", "100"))
    MONGO_MIN_POOL_SIZE: int = int(os.getenv("MONGO_MIN_POOL_SIZE", "10"))

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_POOL_SIZE: int = int(os.getenv("REDIS_POOL_SIZE", "100"))
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "60"))
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )


config = Config()

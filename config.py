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


config = Config()

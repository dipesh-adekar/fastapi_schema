from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import users
from app.db.mongo_db import MongoDB
from app.db.redis import RedisManager
from config import config


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await MongoDB.get_database()
    await RedisManager.get_client()
    yield
    await MongoDB.close()
    await RedisManager.close()


app = FastAPI(
    title="Sample App",
    description="This is a sample app.",
    version="1.0.0",
    docs_url=f"/api/v1/{config.SERVICE_NAME}/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-API-Version", "X-API-Version-Status"],
)

app.include_router(users.router, prefix=f"/api/v1/{config.SERVICE_NAME}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        loop="uvloop",
        http="httptools",
    )

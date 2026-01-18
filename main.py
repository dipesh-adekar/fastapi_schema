from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

from config import config
from app.api.v1.routes import users
from app.db.mongo_db import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.get_database()  # type: ignore
    yield
    await MongoDB.close()


app = FastAPI(
    title="Sample App",
    description="This is a sample app.",
    version="1.0.0",
    docs_url="/api/v1/{}/docs".format(config.SERVICE_NAME),
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

app.include_router(users.router, prefix="/api/v1/{}".format(config.SERVICE_NAME))

if __name__ == "__main__":
    uvicorn.run(  # type: ignore
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        loop="uvloop",
        http="httptools",
    )

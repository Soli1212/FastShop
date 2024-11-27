from fastapi import FastAPI
from Application.Database.connection import init_db
from Application.RedisDB.connection import RedisConnection

from Application.Auth.Authorize import Authorize

from Presentation import UserRouter

app = FastAPI()

app.include_router(router = UserRouter, prefix = "/user")


@app.on_event("startup")
async def startup():
    await init_db()
    await RedisConnection.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await RedisConnection.close()

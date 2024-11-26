from fastapi import FastAPI, Depends, Response, Request
from Application.Database.connection import init_db, get_db
from Application.RedisDB.connection import RedisConnection

from Application.Auth.Authorize import Authorize

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()
    await RedisConnection.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await RedisConnection.close()

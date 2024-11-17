from fastapi import FastAPI, Depends
from Application.Database.connection import init_db, get_db

from datetime import timedelta, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

    

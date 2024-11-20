from fastapi import FastAPI, Depends, Response, Request
from Application.Database.connection import init_db, get_db
from Application.Database.repositories import UserRepositories
from Application.Database.repositories import VCodeRepositories
from Application.Services.UserService import UserServices
from Domain.schemas.UserSchemas import UserCreate, VerifyCode
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()


@app.post("/reg")
async def test(NewUserData: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    reg = await UserServices.Verify_New_User(db = db, response = response, NewUserData = NewUserData)
    return reg

@app.post("/cm")
async def cm(response: Response, request: Request, VerifyData: VerifyCode, db: AsyncSession = Depends(get_db)):
    return await UserServices.Create_New_User(
        db = db,
        response = response,
        request = request,
        VerifyData = VerifyData
    )
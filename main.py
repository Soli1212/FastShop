from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from Application.Database.connection import init_db
from Application.RedisDB.connection import RedisConnection
from Presentation import UserRouter
from Presentation import AddressRouter

from Application.Database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Events --------------------------------
@app.on_event("startup")
async def startup():
    await init_db()
    await RedisConnection.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    await RedisConnection.close()

# Routers ------------------------------
app.include_router(router=UserRouter, prefix="/user")
app.include_router(router=AddressRouter, prefix="/address")

# Middlewares --------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    LogoutDepends = [
        "/user/sing-UP", "/user/singUP",
        "/user/singIN", "/user/forget-Pass",
        "/user/forget-Pass", "/user/change-Pass",
    ]
    if request.url.path in LogoutDepends:
        access_token = request.cookies.get("AccessToken", None)
        refresh_token = request.cookies.get("RefreshToken", None)

        if access_token and refresh_token:
            return RedirectResponse(url="/user/me", status_code=302)

    return await call_next(request)

# Root Endpoint ------------------------
@app.get("/")
async def get(db: AsyncSession = Depends(get_db)):
    uid = "b85b4398-f743-4293-9e86-19b0c81d824c"
    return await AddressRepositories.Get_Address_Count(db, uid)

@app.get("/a")
async def get(db: AsyncSession = Depends(get_db)):
    return await AddressRepositories.Delete_Address(db, 14, "b85b4398-f743-4293-9e86-19b0c81d824c")
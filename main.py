from fastapi import FastAPI, Request, Depends, Path, Query
from fastapi.responses import RedirectResponse

from Application.Database.connection import init_db
from Application.RedisDB.connection import RedisConnection

from Presentation import UserRouter
from Presentation import AddressRouter
from Presentation import TagRouter
from Presentation import ProductRouter

from Application.Database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


from typing import Optional
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
app.include_router(router=TagRouter, prefix="/tags")
app.include_router(router=ProductRouter, prefix="/products")

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
async def pr(db: AsyncSession = Depends(get_db)):
    return "hi 😃"



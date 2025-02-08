from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from Application.Auth import Authorize
from Application.Database.connection import get_db, init_db
from Application.RedisDB.connection import RedisConnection
from Domain.schemas.Cart import CartItem
from Presentation import AddressRouter, CartRouter, ProductRouter, TagRouter, UserRouter

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
app.include_router(router=CartRouter, prefix="/cart")


# Middlewares --------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    LogoutDepends = [
        "/user/sing-up",
        "/user/singup",
        "/user/singin",
        "/user/forget-pass",
        "/user/forget-Pass",
        "/user/change-pass",
    ]
    if request.url.path in LogoutDepends:
        access_token = request.cookies.get("AccessToken", None)
        refresh_token = request.cookies.get("RefreshToken", None)

        if access_token and refresh_token:
            return RedirectResponse(url="/user/me", status_code=302)

    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Root Endpoint ------------------------

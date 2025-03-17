from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from Application.Auth import authorize
from Application.Database.connection import get_db, init_db
from Application.Database.models import Discounts
from Application.Payment.zarinpal_pay import ZarinPalPayment
from Application.RedisDB.connection import RedisConnection
from Application.RedisDB.RedisServices import temp_order_service
from Presentation import (AddressRouter, CartRouter, OrderRouter,
                          ProductRouter, TagRouter, UserRouter)

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
app.include_router(UserRouter, prefix="/user", tags=["user"])
app.include_router(AddressRouter, prefix="/address", tags=["address"])
app.include_router(TagRouter, prefix="/tags", tags=["tags"])
app.include_router(ProductRouter, prefix="/products", tags=["products"])
app.include_router(CartRouter, prefix="/cart", tags=["cart"])
app.include_router(OrderRouter, prefix="/order", tags=["order"])


# Middlewares --------------------------
LOGOUT_DEPENDS = {
    "/user/sing-up",
    "/user/singup",
    "/user/singin",
    "/user/forget-pass",
    "/user/forget-Pass",
    "/user/change-pass",
}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.url.path in LOGOUT_DEPENDS:
        access_token = request.cookies.get("AccessToken")
        refresh_token = request.cookies.get("RefreshToken")

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
@app.get("/")
async def root(request: Request, auth: authorize = Depends(), db: get_db = Depends()):
    return "hi"

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler

from Application.Auth import authorize
from Application.Database.connection import get_db, init_db
from Application.RedisDB.connection import RedisConnection
from Presentation import (
    AddressRouter,
    CartRouter,
    OrderRouter,
    ProductRouter,
    TagRouter,
    UserRouter,
)
from utils import limiter

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Config RateLimiter---------------------------------------

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)


# Root Endpoint ------------------------
@app.get("/")
async def root(request: Request, auth: authorize = Depends(), db: get_db = Depends()):
    return "hi"

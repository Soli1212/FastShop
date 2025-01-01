from fastapi import Request, Response, HTTPException
from datetime import datetime
from hashlib import sha256
from uuid import uuid4
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from Application.Database.repositories import TagRepositories
from Domain.Errors.Tag import PageNotFound


class TagServices:
    @staticmethod
    async def Get_Tags(db: AsyncSession):
        return await TagRepositories.Get_Tags(db = db)

    @staticmethod
    async def Get_Tag_Products(db: AsyncSession, filters: dict, tag_id: int, limit: int = 2):
        products = await TagRepositories.Get_Tag_Products(
            db = db, tag_id = tag_id,
            filters = filters, limit = limit
        )

        if not products[0]:
            raise PageNotFound

        total_pages = (products[1] + limit - 1) // limit

        products = [
            {"id": id, "name": name, "price": price, "images": images or None}
            for id, name, price, images in products[0]
        ]

        return {
            "total_pages": total_pages,
            "products": products
        }

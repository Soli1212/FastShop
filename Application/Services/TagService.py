from sqlalchemy.ext.asyncio import AsyncSession
from Application.Database.repositories import TagRepositories
from Domain.Errors.Tag import PageNotFound


class TagServices:
    @staticmethod
    async def Get_Tags(db: AsyncSession):
        return await TagRepositories.Get_Tags(db = db)

    @staticmethod
    async def Get_Tag_Products(db: AsyncSession, filters: dict, tag_id: int, limit: int = 2):
        TagProducts = await TagRepositories.Get_Tag_Products(
            db = db, tag_id = tag_id,
            filters = filters, limit = limit
        )

        if not TagProducts[0]:
            raise PageNotFound

        products = [
            {"id": id, "name": name, "price": price, "discounted_price":discounted_price, "images": images or None}
            for id, name, price, discounted_price, images in TagProducts[0]
        ]

        return {
            "next_page": TagProducts[1],
            "products": products
        }

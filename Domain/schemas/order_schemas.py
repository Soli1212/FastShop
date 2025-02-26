from typing import Optional

from pydantic import BaseModel, Field


class Order(BaseModel):
    address_id: int = Field(...)
    discount_code: Optional[str] = Field(None)

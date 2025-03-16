import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4, BaseModel, Field, validator


class CartItem(BaseModel):
    product_id: int = Field(..., gt=0)
    size: Optional[int] = Field(None, gt=0)
    color_id: Optional[int] = Field(None)
    quantity: int = Field(..., ge=1)

    @validator("size")
    def validate_size(cls, v):
        if v is not None and v <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size must be greater than 0.",
            )
        return v

    @validator("quantity")
    def validate_quantity(cls, v):
        if v < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be at least 1.",
            )
        return v


class DeleteItem(BaseModel):
    product_id: int = Field(..., gt=0)
    size: Optional[int] = Field(None, gt=0)
    color_id: Optional[int] = Field(None)

    @validator("size")
    def validate_size(cls, v):
        if v is not None and v <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size must be greater than 0.",
            )
        return v

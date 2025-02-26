import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4, BaseModel, Field, validator


class CartItem(BaseModel):
    product_id: int = Field(..., gt=0)
    size: Optional[int] = Field(None, gt=0)
    color: Optional[str] = Field(None)
    quantity: int = Field(..., ge=1)

    @validator("size")
    def validate_size(cls, v):
        if v is not None and v <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size must be greater than 0.",
            )
        return v

    @validator("color")
    def validate_color(cls, v):
        if v:
            hex_color_regex = r"^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            if not re.match(hex_color_regex, v):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid color format. It must be a valid hex color code (e.g., #ff5733).",
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
    color: Optional[str] = Field(None)

    @validator("size")
    def validate_size(cls, v):
        if v is not None and v <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size must be greater than 0.",
            )
        return v

    @validator("color")
    def validate_color(cls, v):
        if v:
            hex_color_regex = r"^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
            if not re.match(hex_color_regex, v):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid color format. It must be a valid hex color code (e.g., #ff5733).",
                )
        return v

from pydantic import BaseModel, Field, validator, field_validator
from fastapi import HTTPException
from typing import Optional
import re

class NewAddress(BaseModel):
    province: str = Field(..., max_length=100, description="Province of the address")
    city: str = Field(..., max_length=100, description="City of the address")
    street: str = Field(..., description="Street name and details")
    postal_code: str = Field(..., max_length=10, description="Postal code for the address")
    recipient_phone: str = Field(..., description="Valid Iranian phone number (e.g., 09123456789)")
    full_address: str = Field(..., description="Full address details")

    @field_validator('province', 'city', 'street', 'full_address', mode='before')
    def validate_required_fields(cls, value):
        if not value or len(value.strip()) == 0:
            raise HTTPException(status_code=422, detail="This field is required and cannot be empty.")
        return value

    @field_validator('postal_code')
    def validate_postal_code(cls, value):
        if value and len(value) > 10:
            raise HTTPException(status_code=422, detail="Postal code cannot exceed 10 characters.")
        return value

    @field_validator('recipient_phone')
    def validate_recipient_phone(cls, value):
        if not re.match(r'^09\d{9}$', value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. Must be a valid Iranian phone number.")
        return value


class UpdateAddress(BaseModel):
    province: Optional[str] = Field(None, max_length=100, description="Name of the province")
    city: Optional[str] = Field(None, max_length=100, description="Name of the city")
    street: Optional[str] = Field(None, description="Street address")
    postal_code: Optional[str] = Field(None, max_length=10, description="Postal code")
    recipient_phone: Optional[str] = Field(None, description="Recipient's phone number")
    full_address: Optional[str] = Field(None, description="Full address")

    @validator('postal_code')
    def validate_postal_code(cls, value):
        if value and len(value) > 10:
            raise HTTPException(status_code=422, detail="Postal code cannot exceed 10 characters.")
        return value

    @validator('recipient_phone')
    def validate_recipient_phone(cls, value):
        if value and not search(r'^09\d{9}$', value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. Must be a valid Iranian phone number.")
        return value

class AddressID(BaseModel):
    id: int

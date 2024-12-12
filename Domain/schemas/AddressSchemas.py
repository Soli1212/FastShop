from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class NewAddress(BaseModel):
    province: str = Field(..., max_length=100, description="Province of the address")
    city: str = Field(..., max_length=100, description="City of the address")
    street: str = Field(..., description="Street name and details")
    postal_code: str = Field(None, max_length=10, description="Postal code for the address")
    recipient_phone: str = Field(..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    full_address: str = Field(..., description="Full address details")

    class Config:
        orm_mode = True

class UpdateAddress(BaseModel):
    province: Optional[str] = Field(None, max_length=100, description="Name of the province")
    city: Optional[str] = Field(None, max_length=100, description="Name of the city")
    street: Optional[str] = Field(None, description="Street address")
    postal_code: Optional[str] = Field(None, max_length=10, description="Postal code")
    recipient_phone: Optional[str] = Field(None, max_length=11, description="Recipient's phone number")
    full_address: Optional[str] = Field(None, description="Full address")

    class Config:
        orm_mode = True

class AddressID(BaseModel):
    id: int
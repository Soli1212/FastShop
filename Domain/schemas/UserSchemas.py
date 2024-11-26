from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class UserCreate(BaseModel):
    fullname: str = Field(..., pattern = r"^[آ-ی\s]+$", min_length=3, max_length=50, description="Full name of the user")
    phone: str = Field(..., pattern = r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    email: Optional[EmailStr] = Field(None, description="Valid email address", max_length=50)
    gender: Optional[GenderEnum] = Field(None, description="Gender of the user")
    age: Optional[int] = Field(None, ge=1, le=120, description="Age of the user (1-120)")

class VerifyCode(BaseModel):
    phone: str = Field( ..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    code: str = Field( ..., pattern=r"^\d{5}$", description="A 5-digit verification code consisting only of numbers")

class UserPhone(BaseModel):
    phone: str = Field( ..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
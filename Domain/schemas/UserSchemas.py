from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from re import search

class UserCreate(BaseModel):
    
    phone: str = Field(..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    fullname: str = Field(..., pattern=r"^[آ-ی\s]+$", min_length=3, max_length=50, description="Full name of the user")
    email: Optional[EmailStr] = Field(None, description="Valid email address", max_length=50)
    password: str = Field(..., min_length=8, max_length=64, description="Password with at least 8 characters including an uppercase letter, a lowercase letter, a number, and a special character")
    
    @validator('password')
    def validate_password(cls, value):
        if not search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        if not search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character')
        return value

class VerifyCode(BaseModel):
    phone: str = Field(..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    code: str = Field(..., pattern=r"^\d{5}$", description="A 5-digit verification code consisting only of numbers")

class UserLogin(BaseModel):
    phone: str = Field(..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    password: str = Field(..., min_length=8, max_length=64, description="Password with at least 8 characters including an uppercase letter, a lowercase letter, a number, and a special character")

    @validator('password')
    def validate_password(cls, value):
        if not search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        if not search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least one special character')
        return value

class UserPhone(BaseModel):
    phone: str = Field(..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")

class ChangePassword(BaseModel):
    phone: str = Field(..., pattern=r"^09\d{9}$", description="Valid Iranian phone number (e.g., 09123456789)")
    code: str = Field(..., pattern=r"^\d{5}$", description="A 5-digit verification code consisting only of numbers")
    password: str = Field(..., min_length=8, max_length=64, description="Password with at least 8 characters including an uppercase letter, a lowercase letter, a number, and a special character")
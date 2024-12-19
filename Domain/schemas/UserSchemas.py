from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from re import search

class UserCreate(BaseModel):
    phone: str = Field(..., description="Valid Iranian phone number (e.g., 09123456789)")
    password: str = Field(..., description="Password with at least 8 characters including an uppercase letter, a lowercase letter, a number, and a special character")
    
    @validator('phone')
    def validate_phone(cls, value):
        if not search(r"^09\d{9}$", value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. It should be like 09123456789.")
        return value

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 64:
            raise HTTPException(status_code=422, detail="Password must be between 8 and 64 characters.")
        if not search(r'[A-Z]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one uppercase letter.")
        if not search(r'[a-z]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one lowercase letter.")
        if not search(r'\d', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one number.")
        if not search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one special character.")
        return value

class UserLogin(BaseModel):
    phone: str = Field(..., description="Valid Iranian phone number (e.g., 09123456789)")
    password: str = Field(..., description="Password with at least 8 characters including an uppercase letter, a lowercase letter, a number, and a special character")
    
    @validator('phone')
    def validate_phone(cls, value):
        if not search(r"^09\d{9}$", value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. It should be like 09123456789.")
        return value

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 64:
            raise HTTPException(status_code=422, detail="Password must be between 8 and 64 characters.")
        if not search(r'[A-Z]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one uppercase letter.")
        if not search(r'[a-z]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one lowercase letter.")
        if not search(r'\d', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one number.")
        if not search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one special character.")
        return value

class UserPhone(BaseModel):
    phone: str = Field(..., description="Valid Iranian phone number (e.g., 09123456789)")
    
    @validator('phone')
    def validate_phone(cls, value):
        if not search(r"^09\d{9}$", value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. It should be like 09123456789.")
        return value

class VerifyCode(BaseModel):
    phone: str = Field(..., description="Valid Iranian phone number (e.g., 09123456789)")
    code: str = Field(..., description="A 5-digit verification code consisting only of numbers")
    
    @validator('phone')
    def validate_phone(cls, value):
        if not search(r"^09\d{9}$", value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. It should be like 09123456789.")
        return value

    @validator('code')
    def validate_code(cls, value):
        if not search(r"^\d{5}$", value):
            raise HTTPException(status_code=422, detail="Code must be a 5-digit number.")
        return value

class ChangePassword(BaseModel):
    phone: str = Field(..., description="Valid Iranian phone number (e.g., 09123456789)")
    code: str = Field(..., description="A 5-digit verification code consisting only of numbers")
    password: str = Field(..., description="Password with at least 8 characters including an uppercase letter, a lowercase letter, a number, and a special character")
    
    @validator('phone')
    def validate_phone(cls, value):
        if not search(r"^09\d{9}$", value):
            raise HTTPException(status_code=422, detail="Invalid phone number format. It should be like 09123456789.")
        return value

    @validator('code')
    def validate_code(cls, value):
        if not search(r"^\d{5}$", value):
            raise HTTPException(status_code=422, detail="Code must be a 5-digit number.")
        return value

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 64:
            raise HTTPException(status_code=422, detail="Password must be between 8 and 64 characters.")
        if not search(r'[A-Z]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one uppercase letter.")
        if not search(r'[a-z]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one lowercase letter.")
        if not search(r'\d', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one number.")
        if not search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise HTTPException(status_code=422, detail="Password must contain at least one special character.")
        return value

class UpdateProfile(BaseModel):
    fullname: Optional[str] = Field(None, description="نام کامل باید فقط شامل حروف فارسی باشد و بین ۲ تا ۵۰ کاراکتر باشد.")
    email: Optional[str] = Field(None, description="یک آدرس ایمیل معتبر وارد کنید.")
    
    @validator('fullname')
    def validate_fullname(cls, value):
        if not search(r"^[\u0600-\u06FF\s]{2,50}$", value):
            raise HTTPException(status_code=422, detail="Fullname must only contain Persian letters and be between 2 to 50 characters.")
        return value

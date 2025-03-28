import re
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, validator


class UserPhone(BaseModel):
    phone: str = Field(
        ..., description="Valid Iranian phone number (e.g., 09123456789)"
    )

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(r"^09\d{9}$", value):
            raise HTTPException(
                status_code=422,
                detail="Invalid phone number format. It should be like 09123456789.",
            )
        return value


class VerifyData(BaseModel):
    phone: str = Field(
        ..., description="Valid Iranian phone number (e.g., 09123456789)"
    )
    code: str = Field(
        ..., description="A 5-digit verification code consisting only of numbers"
    )

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(r"^09\d{9}$", value):
            raise HTTPException(
                status_code=422,
                detail="Invalid phone number format. It should be like 09123456789.",
            )
        return value

    @validator("code")
    def validate_code(cls, value):
        if not re.match(r"^\d{5}$", value):
            raise HTTPException(
                status_code=422, detail="Code must be a 5-digit number."
            )
        return value


class UpdateProfile(BaseModel):
    fullname: Optional[str] = Field(
        None,
        description="نام کامل باید فقط شامل حروف فارسی باشد و بین ۲ تا ۵۰ کاراکتر باشد.",
    )
    email: Optional[EmailStr] = Field(
        None, description="یک آدرس ایمیل معتبر وارد کنید."
    )

    @validator("fullname")
    def validate_fullname(cls, value):
        if not re.match(r"^[\u0600-\u06FF\s]{2,50}$", value):
            raise HTTPException(
                status_code=422,
                detail="Fullname must only contain Persian letters and be between 2 to 50 characters.",
            )
        return value

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from Application.Database import BaseModel


class VerificationCodes(BaseModel):
    __tablename__ = "verificationCodes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    phone = Column(String, unique=True, index=True)
    
    code = Column(String)
    
    expiration_time = Column(DateTime)

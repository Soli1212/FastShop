from Application.Database.models import VerificationCodes
from Domain.Errors.auth import SendedCode
from Domain.Errors.auth import ExpiredCode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from random import randint
from datetime import datetime, timedelta
from hashlib import sha256
from datetime import datetime

class VCodeRepositories:

    @staticmethod
    async def new_verification_code(db: AsyncSession, phone: str):
        query = select(VerificationCodes).where(
            VerificationCodes.phone == phone
        )
        randcode = str(randint(10000, 99999)).encode('utf-8')
        result = await db.execute(query)
        if code := result.scalars().first():
            if code.expiration_time > datetime.utcnow():
                raise SendedCode
            code.code = sha256(randcode).hexdigest()
            code.expiration_time = datetime.utcnow() + timedelta(minutes = 2)
        else:
            NewCode = VerificationCodes(
                phone = phone,
                code = sha256(randcode).hexdigest(),
                expiration_time = datetime.utcnow() + timedelta(minutes = 2)
            )
            db.add(NewCode)
        return randcode.decode('utf-8')
    
    async def get_verification_code(db: AsyncSession, phone: str) -> str:
        query = select(VerificationCodes).where(
            VerificationCodes.phone == phone
        )
        result = await db.execute(query)
        if VerifyData := result.scalars().first():
            if VerifyData.expiration_time > datetime.utcnow():
                return VerifyData.code
            else:
                raise ExpiredCode
        else:
            return None 
        
    async def delete_verification_code(db: AsyncSession, phone: str) -> str:
        query = select(VerificationCodes).where(
            VerificationCodes.phone == phone
        )
        result = await db.execute(query)
        if data := result.scalars().first():
            await db.delete(data)
            



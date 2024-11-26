from random import randint
from datetime import datetime, timedelta
from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Application.Database.models import VerificationCodes
from Domain.Errors.Vcode import SendedCode, ExpiredCode


class VCodeRepositories:

    @staticmethod
    async def new_verification_code(db: AsyncSession, phone: str):
        query = select(VerificationCodes).where(VerificationCodes.phone == phone)
        randcode = str(randint(10000, 99999)).encode('utf-8')
        result = await db.execute(query)

        if code := result.scalars().first():
            if code.expiration_time > datetime.utcnow():
                raise SendedCode

            code.code = sha256(randcode).hexdigest()
            code.expiration_time = datetime.utcnow() + timedelta(minutes=2)

        else:
            new_code = VerificationCodes(
                phone=phone,
                code=sha256(randcode).hexdigest(),
                expiration_time=datetime.utcnow() + timedelta(minutes=2)
            )
            db.add(new_code)

        return randcode.decode('utf-8')


    @staticmethod
    async def get_verification_code(db: AsyncSession, phone: str) -> str:
        query = select(VerificationCodes).where(VerificationCodes.phone == phone)
        result = await db.execute(query)

        if verify_data := result.scalars().first():
            if verify_data.expiration_time > datetime.utcnow():
                return verify_data.code

            raise ExpiredCode

        return None


    @staticmethod
    async def delete_verification_code(db: AsyncSession, phone: str):
        query = select(VerificationCodes).where(VerificationCodes.phone == phone)
        result = await db.execute(query)

        if data := result.scalars().first():
            await db.delete(data)

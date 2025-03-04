from typing import Optional
from fastapi import HTTPException
from httpx import AsyncClient
from pydantic import BaseModel

from Domain.Errors.payment import PaymentFailed
from Domain.Errors.payment import TransactionAlreadyVerified


class PaymentConfig(BaseModel):
    merchant_id: str
    amount: Optional[int] = None
    description: Optional[str] = None
    callback_url: Optional[str] = None
    authority: Optional[str] = None


class ZarinPalPayment:
    def __init__(self):
        self.base_url = "https://sandbox.zarinpal.com/pg/v4/payment"
        self.headers = {"Content-Type": "application/json"}
        
        self.config = PaymentConfig(
            merchant_id="1344b5d4-0048-11e8-94db-005056a205be",
            callback_url="http://127.0.0.1:8000/order/confirmation",
        )

    async def create_payment(self, toman_amount: int) -> str:
        try:
            rial_amount = toman_amount * 10
            data = self.config.dict()
            data.update(
                {"amount": rial_amount, "description": f"Payment {toman_amount} Toman"}
            )

            async with AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/request.json", json=data, headers=self.headers
                )

                result = response.json()
                if response.status_code != 200 or result["data"]["code"] != 100:
                    raise PaymentFailed

                return f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

    async def verify_payment(self, toman_amount: int, authority: str, status: str) -> str:
        rial_amount = toman_amount * 10
        data = self.config.dict()
        data.update({"amount": rial_amount, "authority": authority})

        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/verify.json", json=data, headers=self.headers
            )

            result = response.json()
            if response.status_code != 200 or status == "NOK":
                raise PaymentFailed
            
            match result["data"]["code"]:
                case 100:
                    return result["data"]["ref_id"]

                case 101:
                    raise TransactionAlreadyVerified
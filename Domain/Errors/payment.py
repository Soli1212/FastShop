from fastapi import HTTPException, status


class PaymentFailed(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unfortunately, the payment was unsuccessful !",
        )

class TransactionAlreadyVerified(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This transaction has already been verified !",
        )

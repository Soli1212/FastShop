from fastapi import HTTPException, status


class InvalidDiscountCode(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The discount code is not valid",
        )


class DiscountLimit(HTTPException):
    def __init__(self, limit: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The discount limit is {limit} Tomans",
        )


class UnauthorizeDiscount(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"There are discounted items in your cart. You are not allowed to use a discount code for discounted products",
        )

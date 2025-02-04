from fastapi import HTTPException, status


class NonExistent(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This variant is out of stock or insufficient quantity.",
        )


class ProductNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The product was not found in your cart",
        )

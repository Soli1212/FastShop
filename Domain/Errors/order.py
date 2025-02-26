from fastapi import HTTPException, status


class ProductNotFound(HTTPException):
    def __init__(self, product_id):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} Not Found",
        )


class ProductNotAvalible(HTTPException):
    def __init__(self, product_id: int, color: str, size: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} is not available in color {color} and size {size}",
        )


class InsufficientInventory(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The stock of product {product_id} is not enough for this quantity",
        )

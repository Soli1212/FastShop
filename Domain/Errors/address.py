from fastapi import HTTPException, status


class AddressLimit(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum number of addresses a user can register is 3.",
        )


class NoAddressWasFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="No address was found."
        )


class InvalidProvince(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter a valid province",
        )


class AddressNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Address Not Found !",
        )


class ActiveOrderAddress(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You have an active order with this address and cannot delete it at this time.",
        )

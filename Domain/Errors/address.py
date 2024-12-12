from fastapi import HTTPException, status


class AddressLimit(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "The maximum number of addresses a user can register is 3."
        )

class NoAddressWasFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No address was found."
        )

from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status

class PhoneNumberIsExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="This phone number has been registered")
        
class EmailIsExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="This email has been registered")

class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found !")

class EmptyValues(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Empty Values")

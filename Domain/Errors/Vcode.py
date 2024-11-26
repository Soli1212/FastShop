from fastapi import HTTPException, status

class SendedCode(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="A code has already been submitted, please try again later")


class ExpiredCode(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="The code has expired")
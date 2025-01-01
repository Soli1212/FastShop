from fastapi import HTTPException, status

class PageNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found or no more products available.")
        
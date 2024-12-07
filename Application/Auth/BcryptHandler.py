from bcrypt import hashpw
from bcrypt import gensalt
from bcrypt import checkpw

class BcryptHandler:

    @staticmethod
    def Hash(password: str) -> str:
        return hashpw(
            password = password.encode('utf-8'),
            salt = gensalt()
        ).decode("utf-8")
    

    @staticmethod
    def check(password: str, hashed_password: str) -> bool:
        return checkpw(
            hashed_password = hashed_password.encode('utf-8'),
            password = password.encode("utf-8")
        )
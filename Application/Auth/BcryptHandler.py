from bcrypt import checkpw, gensalt, hashpw


class BcryptHandler:
    """Handler for hashing and verifying passwords using bcrypt."""

    def __init__(self, password: str) -> None:
        self.password = password.encode("utf-8")

    def hash_password(self) -> str:
        """Hash the password and return it as a UTF-8 string."""
        return hashpw(self.password, gensalt()).decode("utf-8")

    def verify_password(self, hashed_password: str) -> bool:
        """Compare the input password with the stored hashed password."""
        return checkpw(self.password, hashed_password.encode("utf-8"))

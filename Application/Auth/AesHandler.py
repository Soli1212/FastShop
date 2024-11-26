from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from hashlib import sha256
from json import dumps, loads
from datetime import timedelta, datetime
from dotenv import load_dotenv
from os import getenv

from Domain.Errors.auth import LoginAgain, DecryptionFailed

load_dotenv()

AES_KEY = getenv("AES_KEY")


class AESHandler:
    def __init__(self, salt: str) -> None:
        self.key = sha256((AES_KEY + salt).encode('utf-8')).digest()


    def encrypt(self, payload: dict, exp: int = 3) -> str:
        cipher = AES.new(self.key, AES.MODE_CBC)
        payload["exp"] = (datetime.utcnow() + timedelta(minutes=exp)).isoformat()
        string_payload = dumps(payload).encode("utf-8")
        cipher_data = cipher.iv + cipher.encrypt(pad(string_payload, AES.block_size))
        return b64encode(cipher_data).decode("utf-8")


    def decrypt(self, encrypted_data: str) -> dict:
        encrypted_bytes = b64decode(encrypted_data)
        iv = encrypted_bytes[:AES.block_size]
        encrypted_payload = encrypted_bytes[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        try:
            decrypted_payload = unpad(cipher.decrypt(encrypted_payload), AES.block_size)
            payload = loads(decrypted_payload.decode("utf-8"))
            if datetime.fromisoformat(payload["exp"]) < datetime.utcnow():
                raise LoginAgain
            payload.pop("exp")
            return payload
        except Exception:
            raise DecryptionFailed

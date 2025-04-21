from datetime import datetime, timedelta

import bcrypt
import jwt


class JWTService:

    def __init__(self, settings):
        self.settings = settings

    def encode(self):
        to_encode = self.settings.payload.copy()
        now = datetime.utcnow()
        if self.settings.expire_timedelta:
            expire = now + self.settings.expire_timedelta
        else:
            expire = now + timedelta(minutes=self.settings.expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            self.settings.private_key,
            algorithm=self.settings.algorithm,
        )
        return encoded

    def decode_jwt(self) -> dict:
        decoded = jwt.decode(
            self.settings.token,
            self.settings.public_key,
            algorithms=[self.settings.algorithm],
        )
        return decoded


class PasswordManager:

    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )

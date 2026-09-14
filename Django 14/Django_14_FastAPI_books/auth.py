from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt

from passlib.context import CryptContext

SECRET_KEY = "fe9d0852-1c56-4e54-81ca-f9e0cc5cd3b9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto")

def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw, hashed_password)


def create_access_token(
        sub: str,
        role: str,
        expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        ):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])





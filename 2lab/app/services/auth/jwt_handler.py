from app.core.settings import KEY, ALGORITHM, TOKEN_LIFETIME_MIN

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt


def create_token(
    data: dict,
    lifetime: Optional[timedelta] = timedelta(minutes=TOKEN_LIFETIME_MIN)
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (lifetime or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

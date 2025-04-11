from jose import JWTError
# from app.models import User
from fastapi import Depends, HTTPException, status
from app.services.auth.jwt_handler import decode_token
from app.cruds.users import get_user
from schemas import schemas
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(schemas.User(email=email, password=""))
    if user is None:
        raise credentials_exception
    return {
        "id": user.get("id"),
        "email": user.get("email"),
    }

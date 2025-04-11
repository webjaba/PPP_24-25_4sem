from app.schemas import schemas
from services.auth.hashing import verify_password
from services.auth.jwt_handler import create_token, decode_token
from cruds.users import create_user, get_user
from core.settings import TOKEN_LIFETIME_MIN
from app.schemas.token import TokenResponse
from app.services.auth.user import get_current_user

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


@router.post("/sign-up/", status_code=status.HTTP_201_CREATED)
def register(user: schemas.User) -> dict:

    res = create_user(user=user)

    if res["exists"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists",
        )

    return {
        "id": res["id"],
        "email": user.email,
        "token": create_token(
            {"email": user.email}, lifetime=TOKEN_LIFETIME_MIN
        ),
    }


@router.post(
    "/login/", status_code=status.HTTP_200_OK, response_model=TokenResponse
)
def auth(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    user = schemas.User(email=form_data.username, password=form_data.password)
    res = get_user(user=user)

    if not res["exists"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user does not exists",
        )

    if not verify_password(user.password, res["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect password",
        )

    return {
        "id": res["id"],
        "email": res["email"],
        "access_token": create_token(
            {"email": res["email"]}, lifetime=TOKEN_LIFETIME_MIN
        ),
        "token_type": "bearer",
    }


@router.get("/users/me/", status_code=status.HTTP_200_OK)
def check_user(token: str = Depends(oauth2_scheme)) -> dict:
    return get_current_user(token)

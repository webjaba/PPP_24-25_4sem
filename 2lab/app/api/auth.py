from app.schemas.schemas import User

from fastapi import APIRouter


router = APIRouter(prefix="/auth")


@router.post("/sign-up/")
def register(user: User) -> dict:
    return {
        "id": 0,
        "email": "",
        "token": "",
    }


@router.post("/login/")
def auth(user: User) -> dict:
    return {
        "id": 0,
        "email": "",
        "token": "",
    }


@router.get("/users/me/")
def check_user() -> dict:
    return {
        "id": 0,
        "email": "",
    }

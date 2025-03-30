from app.schemas import schemas

from fastapi import APIRouter


router = APIRouter(prefix="/auth")


@router.post("/sign-up/")
def register(user: schemas.User) -> dict:
    return {
        "id": 0,
        "email": "",
        "token": "",
    }


@router.post("/login/")
def auth(user: schemas.User) -> dict:
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

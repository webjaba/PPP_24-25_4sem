from app.schemas import schemas
from app.models.models import User
from app.db.session import SessionLocal
from app.services.auth.hashing import hash_password


db = SessionLocal()


def create_user(user: schemas.User) -> dict:
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        return {"id": db_user.id, "exists": True}

    db_user = User(email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "exists": False}


def get_user(user: schemas.User) -> dict:
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {
            "id": -1,
            "email": "",
            "password": "",
            "exists": False
        }

    return {
        "id": db_user.id,
        "email": db_user.email,
        "password": db_user.password,
        "exists": True
    }

from app.api import auth, parser

from fastapi import FastAPI


router = FastAPI()
router.include_router(auth.router)
router.include_router(parser.router)


def main():
    # Ваш код здесь
    pass


if __name__ == "__main__":
    main()

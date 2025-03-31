from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/db/database.db"
TOKEN_LIFETIME_MIN = 60
KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

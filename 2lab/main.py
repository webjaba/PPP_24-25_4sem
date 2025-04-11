import sys
sys.path.append(__file__[:-7] + "app")
from app.api import auth, parser

from fastapi import FastAPI


app = FastAPI()
app.include_router(auth.router)
app.include_router(parser.router)

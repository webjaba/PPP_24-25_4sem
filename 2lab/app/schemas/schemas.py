from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str


class Site(BaseModel):
    url: str
    max_depth: int
    format: str

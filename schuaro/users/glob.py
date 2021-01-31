from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    username: str
    tag: int
    password: str
    active: bool
    permissions: list[str]

class UserPub(BaseModel):
    username: str
    tag: int
    permissions: list[str]


class ParsedUsername(BaseModel):
    success: bool
    username: str
    tag: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    tag: Optional[str] = None
    expires: Optional[int] = None
    scopes: list[str] = []
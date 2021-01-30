from pydantic import BaseModel
from typing import Optional

class UserData(BaseModel):
    req_scope: str

class User(BaseModel):
    username: str
    tag: int
    email: str
    password: str
    data_dict: dict[str:UserData]



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
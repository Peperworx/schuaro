from os import device_encoding
from pydantic import BaseModel
from typing import Optional
from . import permissions
from enum import Enum



class DeveloperType(Enum):
    NODEV = 0
    ADMIN = 1
    DEVELOPER = 2
    PLAYTESTER = 3
    BETATESTER = 4
    DEVPERSONAL = 6
    
class User(BaseModel):
    username: str
    tag: int
    password: str
    active: bool
    permissions: list[str]
    public: bool
    

class UserMe(BaseModel):
    username: str
    tag: int
    permissions: list[str]
    active: bool
    public: bool
    developer: bool = False
    developer_type: DeveloperType = DeveloperType.NODEV

class UserPub(BaseModel):
    username: str
    tag: int
    developer: bool


class ReservedReason(Enum):
    DEVELOPER = 0
    TESTER = 1
    RELATED = 2
    OTHER = 3


class Reserved(BaseModel):
    reserved: str
    reason: ReservedReason = ReservedReason.DEVELOPER


class ParsedUsername(BaseModel):
    success: bool
    username: str
    tag: int


class UserCreateErrors(Enum):
    NO_ERROR: int = 0
    RESERVED_PREFIX: int = 1
    RESERVED_SUFFIX: int = 2
    RESERVED_NAME: int = 3


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    tag: Optional[str] = None
    expires: Optional[int] = None
    scopes: list[str] = []
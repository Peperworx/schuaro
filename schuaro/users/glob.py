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


class Client(BaseModel):
    client_id: str
    client_secret: str
    permissions: list[str]


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    tag: Optional[str] = None
    expires: Optional[int] = None
    scopes: list[str] = []

class OAuthTokenRequest:
    grant_type: str # Grant Type
    # Other stuff. All Are optional.
    

    # If None, these two (client id and secret) will be loaded
    # From HTTP Basic Auth header. If that is not availble, then fails
    client_id: Optional[str] # Client ID for all requests
    client_secret: Optional[str] # Client secret for all requests

    # Typically use these with external app logins
    code: Optional[str] # Code for authorization code grant
    redirect_uri: Optional[str] # Redirect for authorization code grant

    # "Login with authentication app" is a good example of this.
    device_code: Optional[str] # Device code for Token Request grant
    
    # Applications should automatically refresh a token by sending the refres token
    refresh_token: Optional[str] # Code for refresh token grant

    # Password Grant, client grant, etc all use this
    scope: Optional[str] # Scope for several grant types


    # username and password for password grant. These are only used internally.
    # Other applications should use a authorization code grant that is passed through our internal login.
    username: Optional[str] # Username for password grant
    password: Optional[str] # Password for password grant
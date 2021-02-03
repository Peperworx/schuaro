"""
    This file consists of global dataclasses and enums for schuaro
"""

from pydantic import BaseModel
from typing import Optional
from . import as_form

@as_form
class OAuthTokenRequest(BaseModel):
    """
        Completely epic class for handling all possibilities of a oauth token request.
        This is for handling unparsed data, and should be parsed into a separate class later.
    """

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

class ClientAuthentication(BaseModel):
    """
        Represents a client when making authentication requests
    """

    # The client id
    client_id: str

    # The client secret
    client_secret: str

class ClientDB(BaseModel):
    """
        Represents a client in the database
    """

    # The client ID
    client_id: str

    # The client secret
    client_secret: str

    # The client's permissions
    permissions: list[str]

class Client(BaseModel):
    """
        Represents a client oustide of the database
    """

    # The client ID
    client_id: str

    # The client's permissions
    permissions: list[str]

class UserDB(BaseModel):
    """
        Represents a user in the database
    """

    # The username
    username: str

    # The tag
    tag: int

    # SHA 256 hash of the password
    password: str

    # If the user is active
    active: bool

    # If the user is public
    public: bool

    # Session ID for the user. Allows invalidation of tokens
    session_id: int

    # The user's permissions
    # These are just scopes that the user can be assigned in a token.
    permissions: list[str]

class User(BaseModel):
    """
        Represents a user outside of the database
    """
    
    # The username
    username: str

    # The tag
    tag: int

    # If the user is public
    public: bool

    # The user's permissions
    # These are just scopes that the user can be assigned in a token.
    permissions: list[str]

class TokenPair(BaseModel):
    """
        Represents a access-refresh token pain
    """
    access_token: str
    refresh_token: str
    token_type: str

class AccessToken(BaseModel):
    """
        Represents an access token.
    """

    # Either the username of the user, or the clientid
    username: str

    # The tag of the user. Should be zero for clients
    tag: int

    # The expiry time
    expires: int

    # Scopes granted
    scopes: list[str]

    # Session id. Used to force logout of all tokens
    session_id: int

class RefreshToken(BaseModel):
    """
        Represents a refresh token
    """

    # Either the username of the user, or the clientid
    username: str

    # The tag of the user. Should be zero for clients
    tag: int

    # Scopes granted
    scopes: list[str]

    # Session id. Used to force logout of all tokens
    session_id: int

class AuthCode(BaseModel):
    """
        Represents an OAuth2 authorization code
    """

    # Username of the issued user
    username: str

    # Tag of the issued user
    tag: int

    # Scopes that this authorization code can grant
    scopes: list[str]

    # The expiry time
    expires: int

    # The sessionid of the user
    # This is almost a salt, changing when the user resets their password,
    # asks to, or locks their account.
    session_id: int

    # The redirect_uri of the authcode
    redirect_uri: str

    # The code challenge
    code_challenge: str

    # The code challenge method
    code_challenge_method: str

class TokenResponse(BaseModel):
    """
        Models a token response for a token endpoint
    """

    # The type of token
    token_type: str

    # The number of seconds that it will expire in
    expires_in: int

    # The access token
    access_token: str
    
    # The scope
    scope: str 

    # The refresh token
    refresh_token: str 

@as_form
class LoginRequest(BaseModel):
    """
        Model of a login request
    """

    # The username
    username: str

    # The password
    password: str

    # The redirect uri
    redirect_uri: str

    # The client id
    client_id: str

    # The scope
    scope: str = ""

    # The state
    state: str = ""

    # The code challenge
    code_challenge: str

    # The code challeng method
    code_challenge_method: str
"""
    Pydantic data representations for schuaro
"""

# Pydantic
import pydantic

# Utilities
from schuaro.utilities import as_form

# Optional Typehings
from typing import Optional

@as_form
class OAuthTokenRequest(pydantic.BaseModel):
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
    code_verifier: Optional[str] # Code verifier for authcode grant

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

class DB_User(pydantic.BaseModel):
    """
        Represents a user inside of the database
    """

    # These are the username and the tag.
    # The full username is a combination of username and tag
    # where username#hexidecimal_tag
    # This system allows users to have the name they want,
    # and allows duplicate names without conflicts.
    username: str
    tag: int

    # Email is actually used to log in, instead of username/tag
    # This is easier to remember than username#tag
    email: str

    # This is the hash of a password. NEVER store plaintext
    password: str

    # The session ID is used to validate tokens. When a token is used,
    # we check the token's sessionid and the user's session id
    # If these do not match, we reject the token.
    # This allows users to invalidate other accounts. This is also 
    # re-randomized whenever a password reset request is sent.
    session_id: int


    # Permissions is a list of strings, each one representing a permission
    # in the format of domain:permission
    # This allows schuaro to lock specific users out of features such as 
    # the administrator dashboard and to allow specific users features that
    # some do not have.
    permissions: list[str]


    # The active boolean describes whether the user is active or not.
    # Non active users may not login until a password reset or an email
    # verification is sent
    active: bool

    # The public boolean dictates whether or not the user wants to be visible
    # to other users
    public: bool


@as_form
class LoginRequest(pydantic.BaseModel):
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


class DB_Client(pydantic.BaseModel):
    """
        Represents a client in the database
    """

    # The client id
    client_id: str

    # The client secret
    client_secret: str

    # The permissions
    permissions: list[str]


class AuthCode(pydantic.BaseModel):
    """
        Represents an authcode
    """

    # Username
    username: str

    # Email
    email: str

    # Tag
    tag: int

    # Scopes
    scopes: list[str]

    # Expiry
    expires: int

    # Session id
    session_id: int

    # Redirect uri
    redirect_uri: str

    # code challenge and method
    code_challenge: str
    code_challenge_method: str


class TokenResponse(pydantic.BaseModel):
    """
        Models a token response for a token endpoint
    """

    # The type of token
    token_type: str

    # The number of seconds that it will expire in
    expires: int

    # The access token
    access_token: str
    
    # The scope
    scope: str 

    # The refresh token
    refresh_token: str 
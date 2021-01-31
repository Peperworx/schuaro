from pydantic import BaseModel
from typing import Optional


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
from ..utilities import global_classes
from ..clients import utils as client_utils
from typing import Optional
from fastapi import (
    Request,
    status,
    HTTPException
)






def password(token_request: global_classes.OAuthTokenRequest, request: Request):
    # Retrieve details of the client
    client_details = client_utils.extract_client(token_request,request)

    # Retrive scope details
    scopes = token_request.scope.split() if token_request.scope else []
    
    # If it is none, raise error
    if not client_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no_client_details",
            headers={
                "WWW-Authenticate": f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    
    
    return {}

def authorization_code(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

def client_credentials(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

def refresh_token(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

def device_code(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

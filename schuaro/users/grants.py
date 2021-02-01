from ..utilities import global_classes
from ..clients import utils as client_utils
from typing import Optional
from fastapi import (
    Request,
    status,
    HTTPException
)






async def password(token_request: global_classes.OAuthTokenRequest, request: Request):
    # Retrieve details of the client
    client_details = await client_utils.extract_client(token_request,request)

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
    
    # Verify the client
    client_verify = await client_utils.verify_client(
        client_details.client_id,
        client_details.client_secret
    )

    # If it is none, fail
    if not client_verify:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="client_no_exist",
            headers={
                "WWW-Authenticate": f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    # Now we have validated the client, next is user

    return {}

async def authorization_code(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

async def client_credentials(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

async def refresh_token(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

async def device_code(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

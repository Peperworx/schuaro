from ..utilities import global_classes
from ..clients import utils as client_utils
from . import utils as user_utils
from fastapi import (
    Request,
    status,
    HTTPException
)


async def password(token_request: global_classes.OAuthTokenRequest, request: Request) -> global_classes.TokenResponse:
    """
        Grant for password login.
    """
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
    

    # Confirm that username and password are indeed valid
    if not token_request.username or not token_request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no_username_password",
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
                "WWW-Authenticate":
                    f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    # Verify that the client has permissions for password login
    if "login:password" not in client_verify.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="client_no_permissions",
            headers={
                "WWW-Authenticate":
                    f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    # Now we need to examine the scope, and make sure that the client is capable
    # of issuing these permissions
    for scope in scopes:
        # If the client is unable to issue this permission, fail
        if f"issue:{scope}" not in client_verify.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="client_no_permissions",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
            )
    
    # If we have actually reached this point, the client is valid for performing this operation.
    # Yay!

    # Now lets validate the user, making sure they are able to login
    user_validated = await user_utils.verify_user(token_request.username,token_request.password)
    
    # If the user is not validated, fail
    if not user_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect_credentials",
            headers={
                "WWW-Authenticate": f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    

    # Now we need to verify that the user has the permissions required for this scope
    for scope in scopes:
        # If the user is unable to accept this permission, fail
        if scope not in user_validated.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user_no_permissions",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
            )

    # Now we have confirmed that the user can, in fact, login with this scope, permissions, etc.
    ttl=30
    # Now lets issue a token pair.
    tokens = user_utils.issue_token_pair(
        user_validated,
        scopes=scopes,
        ttl=ttl
    )
    
    # Check tokens
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="token_gen_fault"
        )

    # Generate the response
    ret = {
        "token_type":"bearer",
        "expires_in":ttl*60, # How many seconds till expiry
        "access_token":tokens.access_token,
        "scope": " ".join(scopes), # The scopes
        "refresh_token":tokens.refresh_token # The refresh token
    }

    # And return the tokens
    return tokens

async def authorization_code(token_request: global_classes.OAuthTokenRequest, request: Request) -> global_classes.TokenResponse:
    """
        Function for the OAuth2 Authorization code grant
    """

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
                "WWW-Authenticate":
                    f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    

    # Now we need to verify the client can issue authcodes
    if "login:authcode" not in client_verify.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="client_no_permissions",
            headers={
                "WWW-Authenticate":
                    f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    # Now we need to examine the scope, and make sure that the client is capable
    # of issuing these permissions
    for scope in scopes:
        # If the client is unable to issue this permission, fail
        if f"issue:{scope}" not in client_verify.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="client_no_permissions",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
            )
    

    # Decode the authcode
    authcode = await user_utils.decode_authcode(token_request.code)

    # Check if authcode is valid, failing if not
    if not authcode:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="authcode_invalid",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
        )

    # Verify the authcodes redirect_uri
    if authcode.redirect_uri != token_request.redirect_uri:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="authcode_invalid_redirect",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
        )

    # Now we know the authcode is valid.

    
    # Timetolive of 30 mins
    ttl = 30

    # Lets issue a token
    issued_tokens = await user_utils.issue_token_pair(
        await user_utils.get_user(
            authcode.username,
            authcode.tag
        ),
        ttl=ttl,
        scopes=authcode.scopes
    )

    # Generate the response
    ret = {
        "token_type":"bearer",
        "expires_in":ttl*60, # How many seconds till expiry
        "access_token":issued_tokens.access_token,
        "scope": " ".join(scopes), # The scopes
        "refresh_token":issued_tokens.refresh_token # The refresh token
    }
    
    # Load into model and return
    return global_classes.TokenResponse(**ret)

async def client_credentials(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

async def refresh_token(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

async def device_code(token_request: global_classes.OAuthTokenRequest, request: Request):
    return {}

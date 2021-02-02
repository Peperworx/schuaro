"""
    Handers for the default authcode issuer.
"""
from ..utilities import global_classes
from . import utils as user_utils
from .. import database
from fastapi import (
    Request,
    status,
    HTTPException
)
import hashlib
import urllib.parse
from .. import config

async def login(login_request: global_classes.LoginRequest):
    """
        Basic login for authorization code login
    """
    # Parse scopes
    scopes = login_request.scope.split(" ") if login_request.scope != "" else []
    # Get the database
    db = await database.get_db()

    # Get the collections
    col_clients = db["schuaro-clients"]
    col_users = db["schuaro-users"]

    # Get our client
    our_client = col_clients.find_one({
        "client_id": config.settings.authcode_clientid
    })

    # Verify our client
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="client_no_exist",
            headers={
               "WWW-Authenticate":
                f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    # Verify our client_secret
    if our_client["client_secret"] != config.settings.authcode_clientsecret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="client_no_password",
            headers={
                "WWW-Authenticate":
                    f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )

    # Verify our client has authorization
    if "assign:authcode" not in our_client["permissions"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="client_no_permissions",
            headers={
                "WWW-Authenticate":
                    f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    # Verify our client has requested scopes
    for scope in scopes:
        if f"issue:{scope}" not in our_client["permissions"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="client_no_permissions",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
                }
            )

    # Get the client
    client = col_clients.find_one({
        "client_id": login_request.client_id
    })

    # Fail if non existant
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="client_no_exist",
            headers={
               "WWW-Authenticate":
                f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    
    

    # Verify the client has required scopes
    for scope in scopes:
        if f"issue:{scope}" not in client["permissions"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="client_no_permissions",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
                }
            )

    # Parse the username
    try:
        uname = login_request.username.split("#")[0]
        tag = int(login_request.username.split("#")[1],16)
    except:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username_invalid",
            headers={
               "WWW-Authenticate":
                f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        ) 
    
    # Get the user
    user = await user_utils.get_user(uname,tag)

    # Check user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user_no_exist",
            headers={
               "WWW-Authenticate":
                f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    


    # Check password
    if hashlib.sha256(login_request.password.encode()).hexdigest().lower() != user.password.lower():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user_incorrect_password",
            headers={
               "WWW-Authenticate":
                f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    # Check user has permissions for scopes
    for scope in scopes:
        if scope not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="client_no_permissions",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
                }
            )
    
    # Time To live
    ttl = 30

    # Generate authcode
    authcode = await user_utils.issue_authcode(
        user,
        login_request,
        ttl=ttl,
        scopes=scopes
    )

    # If it failed, fail
    if not authcode:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="authcode_gen_error",
            headers={
                "WWW-Authenticate":
                    f"Bearer{f' scope={login_request.scope}' if len(scopes) > 0 else ''}"
            }
        )

    # If not, generate url
    get_data = {
        "state":login_request.state,
        "code":authcode
    }
    
    # generate url
    redirect_url = f"{login_request.redirect_uri}?{urllib.parse.urlencode(get_data)}"

    return redirect_url
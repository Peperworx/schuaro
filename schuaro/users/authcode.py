"""
    Handers for the default authcode issuer.
"""
from schuaro.utilities import global_classes
from schuaro.users import utils as user_utils
from schuaro.clients import utils as client_utils
from fastapi import (
    status,
    HTTPException
)
import urllib.parse

async def login(login_request: global_classes.LoginRequest):
    """
        Basic login for authorization code login
    """

    # Parse in scopes
    scopes = login_request.scope.split() if login_request.scope != "" else [] 

    # Retrieve the client
    client = await client_utils.get_client(login_request.client_id)

    # If it is none, fail
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no_client"
        )
    
    # Verify the client can login with authcode
    if "assign:authcode" not in client.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="client_no_permissions"
        )
    
    # Verify the client has all required scopes
    for scope in scopes:
        if f"issue:{scope}" not in client.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="client_no_permissions"
            )

    # Now we can verify the user
    user = await user_utils.verify_user(
        login_request.username,
        login_request.password
    )

    # If it is none, fail
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no_user"
        )
    
    # Now we check the user's scopes
    for scope in scopes:
        if f"{scope}" not in user.permissions:
            print(scope)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user_no_permissions"
            )
    

    # Now we can just generate the authcode
    ttl = 30
    authcode = await user_utils.issue_authcode(
        user,
        login_request,
        ttl=ttl,
        scopes=scopes
    )


    # If it is none, fail
    if not authcode:
        # This should never happen
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="issue_failed"
        )
    
    # generate the get data
    get_data = {
        "state": login_request.state,
        "code":authcode
    }

    # Generate url
    redirect_url = f"{login_request.redirect_uri}?{urllib.parse.urlencode(get_data)}"
    
    # Return
    return redirect_url
    
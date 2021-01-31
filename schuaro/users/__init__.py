from fastapi import Depends, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm, 
    SecurityScopes,
)

from pydantic import BaseModel
from fastapi import APIRouter

# Import library for permissions
from . import permissions

# Import library to handle encryption
from . import encryption

# Import library to access database
from . import db

# Import utilites
from . import util

from . import glob






# OAuth2 password bearer scheme
oauth2_password_bearer = OAuth2PasswordBearer(
    tokenUrl="users/token",
    scopes=permissions.scopes
)


# Get the router ready
router = APIRouter(prefix="/users")


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_password_bearer)
    ):
    if security_scopes.scopes:
        authvalue = f"Bearer scope=\"{security_scopes.scope_str}\""
    else:
        authvalue = f"Bearer"
    user = util.decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate":authvalue}
        )
    g_user = db.get_user(
        glob.ParsedUsername(
            success = True,
            username = user.username,
            tag = user.tag
        )
    )
    for scope in security_scopes.scopes:
        if scope not in user.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect permissions",
                headers={"WWW-Authenticate":authvalue}
            )
    return g_user




@router.post(
    "/token",
    response_model=glob.Token)
async def token_auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        OAuth Password Bearer authentication. Returns a token.
    """

    # Parse out the username
    u_parsed = util.parse_username(form_data.username)

    # Verify the user
    u_verify = db.verify_user(u_parsed, form_data.password, form_data.scopes)

    # If not valid, reaise exception
    if u_verify == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify login credentials"
        )
    
    # If we are still here, we need to generate and return a token
    token = util.generate_token(u_verify,form_data,scopes=form_data.scopes)
    print(token)
    # Return the token along with other details
    return token

@router.get("/me")
async def read_users_me(current_user: glob.User = Security(get_current_user,scopes=["me"])):
    

    # Censor the current user's data
    # This is to remove things like password, etc as to lesen
    # security concerns
    cu = glob.UserPub(**dict(current_user))

    # Return
    return cu
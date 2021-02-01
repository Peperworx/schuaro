# FastAPI
from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status,
    Form
)

# FastAPI Security stuff
from fastapi.security import (
    OAuth2PasswordBearer
)

from . import permissions

# Pydantic
from pydantic import BaseModel

# Global data
from ..utilities import global_classes as global_classes

# Grants
from . import grants

# User utilities
from . import utils as user_utils


# Get the router ready
router = APIRouter(prefix="/users")

# Password bearer
# We use this for the sake of swagger
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{router.prefix}{'/' if not router.prefix.endswith('/') else ''}token",
    scopes=permissions.scopes
)


# Use this on top of oauth2_scheme
async def current_user(token: str = Depends(oauth2_scheme)):
    """
        Retrieves the current user from a token.
    """

    # Decode the token
    token_decoded = user_utils.decode_token(token)

    # If it is none, fail
    if not token_decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect_token"
        )
    
    # If not, get the user
    user = user_utils.get_user(
        token_decoded["username"],
        token_decoded["tag"]
    )

    # If none, fail
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect_token"
        )

    # If successful, return
    return user

# Token route. OAuth token support
@router.post("/token")
async def token_auth(
    token_request: global_classes.OAuthTokenRequest = Depends(global_classes.OAuthTokenRequest.as_form), # This one took a lot of googling.
    request: Request = None):
    """
        Token authentication. Supports all OAuth grants.
    """
    # Get the grant_type
    grant_type = token_request.grant_type

    # Basic password grant
    if grant_type == "password":
        return await grants.password(token_request,request)
    elif grant_type == "authorization_code":
        return await grants.authorization_code(token_request,request)
    elif grant_type == "client_credentials":
        return await grants.client_credentials(token_request,request)
    elif grant_type == "refresh_token":
        return await grants.refresh_token(token_request,request)
    elif grant_type == "urn:ietf:params:oauth:grant-type:device_code":
        return await grants.device_code(token_request,request)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unexpected_grant_type"
        )

# Basic test function that requires login
@router.get("/")
async def basic_test(curr_user: global_classes.UserDB = Depends(current_user)):
    """
        Super simple function that requires login token
    """

    print(curr_user)
    return {"hello":"world"}

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

# Get the router ready
router = APIRouter(prefix="/users")

# Password bearer
# We use this for the sake of swagger
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{router.prefix}{'/' if not router.prefix.endswith('/') else ''}token",
    scopes=permissions.scopes
)



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
async def basic_test(token = Depends(oauth2_scheme)):
    """
        Super simple function that requires login token
    """
    print(token)
    return {"hello":"world"}

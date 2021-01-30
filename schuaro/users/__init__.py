from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

from pydantic import BaseModel
from fastapi import APIRouter

# Import library for permissions
from . import permissions

# Import library to access database
from . import db



# Get the router ready
router = APIRouter(prefix="/users")


# OAuth2 password bearer scheme
oauth2_password_bearer = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes = permissions.scopes
)




@router.post("/token")
async def token_auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        OAuth Password Bearer authentication. Returns a token.
    """
    print(form_data.__dict__)
    return {}
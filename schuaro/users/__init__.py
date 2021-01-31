# FastAPI
from fastapi import (
    APIRouter,
    Depends
)

# FastAPI Security stuff
from fastapi.security import (
    OAuth2PasswordBearer
)


# Pydantic
from pydantic import BaseModel


# Get the router ready
router = APIRouter(prefix="/users")

# Password bearer
# We use this for the sake of swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{router.prefix}{'/' if not router.prefix.startswith('/') else ''}token")

@router.get("/token")
def token_auth():
    """
        Token authentication. Supports all OAuth grants.
    """
    
    return {}

@router.get("/")
def basic_test(token = Depends(oauth2_scheme)):
    """
        Super simple function that requires login token
    """
    return {"hello":"world"}

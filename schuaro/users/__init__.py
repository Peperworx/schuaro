from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

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



# Get the router ready
router = APIRouter(prefix="/users")


# OAuth2 password bearer scheme
oauth2_password_bearer = OAuth2PasswordBearer(
    tokenUrl="users/token"
)





async def get_current_user(token: str = Depends(oauth2_password_bearer)):
    user = util.decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    g_user = db.get_user(
        util.ParsedUsername(
            success = True,
            username = user["username"],
            tag = user["tag"]
        )
    )
    return g_user

async def get_current_active_user(current_user: db.User = Depends(get_current_user)):
    
    return current_user


@router.post(
    "/token",
    response_model=util.Token)
async def token_auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        OAuth Password Bearer authentication. Returns a token.
    """

    # Parse out the username
    u_parsed = util.parse_username(form_data.username)

    # Verify the user
    u_verify = db.verify_user(u_parsed, form_data.password)

    # If not valid, reaise exception
    if u_verify == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify login credentials"
        )
    
    # If we are still here, we need to generate and return a token
    token = util.generate_token(u_verify)
    print(token)
    # Return the token along with other details
    return token

@router.get("/me")
async def read_users_me(current_user: db.User = Depends(get_current_active_user)):
    
    return current_user
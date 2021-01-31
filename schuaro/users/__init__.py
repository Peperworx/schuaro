from os import stat
from fastapi import Depends, HTTPException, status, Security, Form, APIRouter, Response
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm, 
    SecurityScopes,
)

# Pydantic
from pydantic import BaseModel


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
    g_user = await db.get_user(
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
    u_verify = await db.verify_user(u_parsed, form_data.password, form_data.scopes)

    # If not valid, reaise exception
    if u_verify == None:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify login credentials"
        )
    
    # If we are still here, we need to generate and return a token
    token = util.generate_token(u_verify,form_data,scopes=form_data.scopes)
    
    # Return the token along with other details
    return token

@router.get("/me")
async def read_users_me(current_user: glob.User = Security(get_current_user,scopes=["me"])):
    

    # Censor the current user's data
    # This is to remove things like password, etc as to lesen
    # security concerns
    cu = glob.UserMe(**dict(current_user))

    # Return
    return cu


@router.get("/user/{username}/{tag}")
async def read_users_other(username:str, tag:str, current_user: glob.User = Security(get_current_user,scopes=["user:read"])):
    """
        Reads another public user. Returns public information.
    """

    # Convert tag to hex. If it fails, raise an error.
    try:
        tagint = int(tag, 16)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Tag must be a hexidecimal string"
        )


    # If we are all good, lets fetch the user
    user = await db.get_user(
        glob.ParsedUsername(
            success=True,
            username=username,
            tag=tagint
        )
    )

    # If it does not exist, raise error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if user is public and raise error if not
    if not user.public:
        # Just a 404, because of hidden user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # If we are all good, return censored user
    # Censored simply means we have removed all data
    # That others do not need to know. Ex: password

    return glob.UserPub(**dict(user))


@router.post("/create")
async def create_user(
    response: Response,
    username: str = Form(default=None),
    password: str = Form(default=None),
    client_id: str = Form(default=None),
    client_secret: str = Form(default=None)
    ):
    """
        Creates a user with default permissions
    """

    # Validate the request. Nothing can be none
    if username == None or password == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uh, you need to supply both a username AND a password"
        )
    
    # Validate clientid
    client_validated = await db.validate_client(client_id,client_secret)
    
    # If unable to validate client, fail
    if not client_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client"
        )

    # Check permissions
    if "grant:user_defaults" not in client_validated.permissions or \
        "create:user" not in client_validated.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client does not have required permissions"
        )
    
    # Now we can continue

    # Lets parse the username.
    uname_parsed = util.parse_username(username)
    
    # If it failed, lets raise an error
    if not uname_parsed.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must supply username and tag like so: username#tag where username is a string, and tag is a hexidecimal value."
        )
    

    # Try to get the user. If we can, we are unable to create.
    gu = await db.get_user(uname_parsed)
    
    if gu:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That tag/username already exists! Choose a new tag"
        )
    
    # If it all works, create the user
    res = await db.create_user(
        uname_parsed,
        password
    )

    # Resolve Errors
    if res == glob.UserCreateErrors.RESERVED_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Whoah there. Your username starts with a reserved prefix! Try something else"
        )
    elif res == glob.UserCreateErrors.RESERVED_SUFFIX:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Whoah there. Your username ends with a reserved suffix! Try something else"
        )
    elif res == glob.UserCreateErrors.RESERVED_NAME:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "Yeah, ummm. Sorry about this, but you are unable to use that username. Try somethign else. :/"
        )
    
    response.status_code = status.HTTP_201_CREATED
    return {
        "success": True
    }

@router.post("/client/generate")
async def generate_client(current_user: glob.User = Security(get_current_user,scopes=["ability:issue_client","ability:administrator"])):
    """
        Generates a client. Requires admin, as client has full admin for now.
    """

    # Generate the client
    client_generated = await db.generate_client()

    return client_generated
"""
    Basic token based login for schuaro
"""

# Fastapi
from fastapi import APIRouter, Request, Depends, Response, status

# Jinja2 stuff
from fastapi.templating import Jinja2Templates

# Data representations
from schuaro.data import rep

# Authcode login
from schuaro.login import authcode


# Ready the api router
router = APIRouter(
    prefix="/login"
)




# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Serve the login template
@router.get("/")
async def login(request: Request):
    """
        Returns a login template
    """
    return templates.TemplateResponse("login.html",{"request":request})

# The login post
@router.post("/", tags=["authentication"])
async def login(
    response: Response,
    login_request: rep.LoginRequest = Depends(rep.LoginRequest.as_form)
    
):
    """
        This is for token login authentication. Super basic authcode issueing
    """
    
    # Get the authcode
    ret = authcode.authenticate(login_request)
    print(ret)


    # Redirect
    #response.status_code = status.HTTP_303_SEE_OTHER
    #response.headers["Location"] = ret
    
    return {}

# Oauth2 Route
@router.post("/oauth2")
async def oauth2(
    login_data: rep.OAuthTokenRequest = Depends(rep.OAuthTokenRequest.as_form)
):
    """
        Route for OAuth2 Authentication.
        Supports authorization code, refresh token, and password flow.
    """
    

    print(login_data)


    return login_data



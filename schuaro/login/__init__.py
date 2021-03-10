"""
    Basic token based login for schuaro
"""

# Fastapi
from fastapi import APIRouter, Request, Depends, Response, status, HTTPException

# Jinja2 stuff
from fastapi.templating import Jinja2Templates

# Data representations
from schuaro.data import rep

# Authcode login
from schuaro.login import authcode

# Urllib parse
import urllib.parse

# Error
from schuaro.errors import *


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
    try:
        code = await authcode.authenticate(login_request)
    except SchuaroException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    # Generate the data
    redirect_data = {
        "code": code,
        "state": login_request.state
    }

    # Redirect
    redirect_url = f"{login_request.redirect_uri}?{urllib.parse.urlencode(redirect_data)}"
    
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = redirect_url
    
    return {}

# Oauth2 Route
@router.post("/oauth2")
async def oauth2(
    request: Request,
    login_data: rep.OAuthTokenRequest = Depends(rep.OAuthTokenRequest.as_form)
):
    """
        Route for OAuth2 Authentication.
        Supports authorization code, refresh token, and password flow.
    """
    

    # Grab the grand type
    grant = login_data.grant_type

    # Switch on the grant
    if grant == "authorization_code":
        return await authcode.grant(login_data, request)



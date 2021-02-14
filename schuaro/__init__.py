from schuaro import utilities
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import schuaro.users
import schuaro.config
import schuaro.party
import schuaro.config
import schuaro.utilities


tags_metadata = [
    {
        "name": "authentication",
        "description": "OAuth2 Authentication",
    },
]

app = FastAPI(
    swagger_ui_init_oauth = {
        "usePkceWithAuthorizationCodeGrant":True
    },
    openapi_tags = tags_metadata
)
# Static files
app.mount("/static",StaticFiles(directory="static"),name="static")


templates = Jinja2Templates(directory="templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Router for users
app.include_router(
    schuaro.users.router
)

# Router for party
app.include_router(
    schuaro.party.router
)


# Route for web login
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})


# We need a route for clients such as video games to use. We are not as worried about security on these
@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    """
        Route for issuing password tokens to user
    """
    
    # Grab our client details
    client_id = schuaro.config.settings.client_id
    client_secret = schuaro.config.settings.client_secret
    
    # Create the request
    token_request = schuaro.utilities.global_classes.OAuthTokenRequest(
        grant_type = "password", # Password grant
        client_id = client_id, # Schuaro's client id
        client_secret = client_secret, # And Schuaro's client secret
        username = username, # The username
        password = password, # The password
    )
    
    # Fake the request by calling the grant function
    tokens = await schuaro.users.grants.password(
        token_request,
        request
    )

    # Return the tokens
    return tokens

# Super basic root
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

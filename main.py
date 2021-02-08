from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import schuaro.users
import schuaro.config
import schuaro.party


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

# Javascript client
app.mount("/client",StaticFiles(directory="client/js"),name="client")

templates = Jinja2Templates(directory="templates")


# Router for users
app.include_router(
    schuaro.users.router
)

# Router for party
app.include_router(
    schuaro.party.router
)

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})

@app.get("/party_test")
async def party_test(request: Request):
    return templates.TemplateResponse("party_test.html",{"request":request})

@app.post("/party_test_login")
async def party_test_login(request: Request):
    """
        This is the preferred example of handling local logins.
        This should exchange an authorization code for a token, and return the token response.
        The reason why we use this, is because it requires a clientid.
    """
    return {}

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

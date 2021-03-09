from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import schuaro.users




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

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Mount users graphql
app.mount("/users",schuaro.users.router)
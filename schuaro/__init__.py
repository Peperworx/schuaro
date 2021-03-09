from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import schuaro.users
import graphene
from starlette.graphql import GraphQLApp





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


# Users API
app.add_route("/users", GraphQLApp(schema=graphene.Schema(query=schuaro.users.Query)))


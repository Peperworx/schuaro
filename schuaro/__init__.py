from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

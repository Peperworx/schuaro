from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import schuaro.users
import schuaro.config


app = FastAPI()

templates = Jinja2Templates(directory="templates")



app.include_router(
    schuaro.users.router
)

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

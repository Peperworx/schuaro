
from schuaro import client
from fastapi import (
    FastAPI,
    Request
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



# Our clientid. set this to your value
client_id = "someid"
# Same for client secret
client_secret = "hashofsomesecret"

sc = client.SchuaroClient(
    "http://localhost:8000/", 
    client_id,
    client_secret
)



# Start an authserver
app = FastAPI()
templates = Jinja2Templates(directory="example/templates")

# Lets display a login with schuaro at /
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    login_data = sc.generate_login_url("http://localhost:5000/callback")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "login_uri":login_data[0]
    })

# Here is our success callback
@app.get("/callback")
def callback(state: str, code: str):
    print(state,code)
    return {

    }
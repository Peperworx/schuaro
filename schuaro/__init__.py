
# Fastapi Core
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

# Schuaro routes
import schuaro.users
import schuaro.login

# Login scheme
from schuaro.login import scheme



# Metadata for tags
tags_metadata = [
]


# Initialize the app
app = FastAPI(
    swagger_ui_init_oauth = {
        "usePkceWithAuthorizationCodeGrant":True
    },
    openapi_tags = tags_metadata
)
# Static files
app.mount("/static",StaticFiles(directory="static"),name="static")



# Mount users graphql
app.mount("/users",schuaro.users.router)

# Login Router
app.include_router(
    schuaro.login.router
)

# Basic / url
@app.get("/")
async def read_items(token: str = Depends(scheme.oauth2_scheme)):
    return {"token": token}
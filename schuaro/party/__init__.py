# Fastapi
from fastapi import (
    APIRouter,
    WebSocket,Security
)

# Global stuff
from schuaro.utilities import global_classes

# login stuff
from schuaro.login import current_user

# Prep router
router = APIRouter(
    prefix="/party",
)


# Invite manager websocket
@router.websocket("/invites")
async def invites(ws: WebSocket, 
    current_user: global_classes.UserDB = Security(current_user,scopes=["ability:party"])
    ):
    # Accept the connection
    await ws.accept()
    
    # Begin loop
    while True:

        # Recieve Data
        data = await ws.receive_json()


        # Send data
        await ws.send_json({"hello":"world"})
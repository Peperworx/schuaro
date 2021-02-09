
from schuaro import client
import time



# Our clientid. set this to your value
client_id = "logintest"

# It is best to leave the client secret out, as long as your client has login permissions

sc = client.SchuaroClient(
    "http://localhost:8000/", 
    client_id,
    None
)


# This is our login callback
def on_login(access_token, refresh_token, expires):
    print(access_token)


# This starts a server, and opens the browser for authentication
sc.initiate_callback(
    on_login, # Specify our login callback
    scope = [
        "me"
    ]
)







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


# This opens a browser for login, and blocks until login is sucessful
sc.login(
    scope = [
        "me"
    ]
)









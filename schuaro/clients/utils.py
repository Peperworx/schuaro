# Retrieve the global_classes from utilities
from ..utilities import global_classes

# Get database utilities
from .. import database

# We need optional from typing, for, well, optional return types
from typing import Optional

# FastAPI stuff
from fastapi import (
    Request
)


# Hashlib for secret hashing
import hashlib

# Base64 for decoding http headers
import base64

async def extract_client(
    token_request: global_classes.OAuthTokenRequest, 
    request: Request) -> Optional[global_classes.ClientAuthentication]:
    """
        A function to extract client details from a token_request
        and a request. Will return None if the client was not provided
    """

    # Check for client id and secret in token_request
    # They will be none if not provided
    client_id = token_request.client_id
    client_secret = token_request.client_secret

    # Now Check for client id and secret in basic auth header
    try:
        if not client_id or not client_secret:
            authHeader = base64.b64decode(request.headers["authorization"].split(" ")[1])
            client_id, client_secret = [a.decode() for a in authHeader.split(b":")]
    except:
        # If we are here, it 100% does not exist in the auth header
        # And it does not exist (fully) in the token request.
        # Return None
        return None
    
    # If it exists, we will have reached this point
    # Lets create the return structure and return
    return global_classes.ClientAuthentication(
        client_id=client_id,
        client_secret=client_secret
    )





async def verify_client(client_id: str, client_secret: str):
    """
        Verifies a client. Returns the value of the client in the database, or none if client was not found.
    """
    
    # Get the db
    db = database.get_db()


    # Grab the clients collection
    col = db["schuaro-clients"]

    # Search for the client_id
    client = col.find_one(
        {
            "client_id":client_id
        }
    )
    
    # If we did not find it return none
    if not client:
        return None
    
    # Convert to a pydantic model
    client = global_classes.ClientDB(**client)

    # Hash the provided secret, and convert to lowercase
    hashed_secret = hashlib.sha256(client_secret.encode()).hexdigest().lower()


    # Compare secrets
    if hashed_secret != client.client_secret.lower():
        # Return none if compare failed
        return None
    
    # If we are here, we are all good! Lets just return the client (without secret, duh)
    return global_classes.Client(**dict(client))

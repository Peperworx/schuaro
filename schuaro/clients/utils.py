from ..utilities import global_classes
from typing import Optional
from fastapi import (
    Request
)
import base64
def extract_client(
    token_request: global_classes.OAuthTokenRequest, 
    request: Request) -> Optional[global_classes.ClientAuthentication]:
    """
        A function to extract client details from a token_request
        and a request. Will return None if the client was not provided
    """

    # Whether or not we found the details
    found: bool = False

    # Check for client id and secret in token_request
    # They will be none if not provided
    client_id = token_request.client_id
    client_secret = token_request.client_secret

    # Now Check for client id and secret in basic auth header
    try:
        if not client_id or not client_secret:
            authHeader = base64.b64decode(request.headers["authorization"].split(" ")[1])
            client_id,client_secret = str(authHeader).split(":")
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
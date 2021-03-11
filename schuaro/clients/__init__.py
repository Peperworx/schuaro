"""
    Code for verifying and managing clients
"""


# Data representations
from schuaro.data import rep

# Database stufflient
import schuaro.data as data

# Utilities
import schuaro.utilities as util

# Errors
from schuaro.errors import *

# Hashlib
import hashlib


async def verify_client_scopes(client: rep.DB_Client, scope: list[str] = []) -> bool:
    """
        Verifies a client. Raises an error if there is something wrong.
    """

    # Verify the client scopes
    for s in scope:
        if f"issue:{s}" not in client.permissions:
            raise ClientInvalid(f"Scope {s} not given to client")

    return True

async def verify_client(client: rep.DB_Client, secret: str, scope: list[str] = []) -> bool:
    """
        Verifies a client. Raises an error if there is something wrong.
    """

    if hashlib.sha256(secret.encode()).hexdigest().lower() != client.client_secret.lower():
        raise ClientInvalid(f"Client Secret invalid")

    # Verify the client scopes
    for s in scope:
        if f"issue:{s}" not in client.permissions:
            raise ClientInvalid(f"Scope {s} not given to client")
    
    return True
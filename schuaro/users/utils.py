"""
    General utilities for users
"""


# Data representations
from schuaro.data import rep

# Database stuff
import schuaro.data as data

# Utilities
import schuaro.utilities as util

# Errors
from schuaro.errors import *

# Hashlib
import hashlib


async def verify_user(user: rep.DB_User, password: str, scope: list[str] = []):
    """
        Verifies a client. Raises an error if there is something wrong.
    """

    # Verify the client scopes
    for s in scope:
        if f"{s}" not in user.permissions:
            raise UserInvalid(f"Scope {s} not given to user")
    
    # Verify the password
    if user.password.lower() != hashlib.sha256(password.encode()).hexdigest().lower():
        raise UserInvalid(f"Invalid password for user {user.username}")

    return True
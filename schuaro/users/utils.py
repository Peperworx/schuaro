# Retrieve the global_classes from utilities
from ..utilities import global_classes

# Optional types
from typing import Optional

# Get database utilities
from .. import database

# Get permissions information
from . import permissions

# Get configuration data
from .. import config

# Hashlib for password hashing
import hashlib

# jose for JWT
from jose import jwt

# Secrets for random codes
import secrets

# Calendar and datetime for time stuff
import calendar
from datetime import datetime, time, timedelta

from schuaro import utilities

async def verify_user(username: str, password: str) -> global_classes.User:
    """
        Verifies a user based on username and password.
        Used mainly for OAuth password authentication
    """

    # Parse the username into a username and a tag
    try:
        uname = username.split("#")[0]
        tag = int(username.split("#")[1],16)
    except:
        # If that tag is not an hexidecimal integer, the user does not exist.
        return None
    
    # Get the db
    db = database.get_db()


    # Grab the users collection
    col = db["schuaro-users"]

    # Find the user
    user = col.find_one(
        {
            "username":uname,
            "tag":tag
        }
    )

    # Verify the user exists
    if not user:
        return None
    
    # Convert to pydantic model
    user = global_classes.UserDB(**user)

    # Hash the given password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Compare the passwords as lowercase, for case insensitivity in the hash
    # We can do this, because the hash is different for differently cased strings
    # So this simply allows forwards and backwards compatibility with different
    # libraries
    if password_hash.lower() != user.password.lower():
        return None
    

    # Return the user, without sensitive information
    return global_classes.User(**user.dict())

def issue_token_pair(user: global_classes.User, ttl: int = 30, scopes: list[str] = permissions.default_permissions) -> Optional[global_classes.TokenPair]:
    """
        Issues an access/refresh token pair.
    """

    # Expires time
    exp_time = datetime.utcnow()+timedelta(minutes=ttl)

    # Dictionary containing data for access token
    access_data = {
        "username":user.username,
        "expires": calendar.timegm(exp_time.timetuple()),
        "scopes":scopes,
        "session_id":user.session_id
    }
    
    
    # Encode it
    access_token = jwt.encode(
        access_data,
        config.settings.secret,
        "HS256"
    )

    # Dictionary containing data for refresh token
    refresh_data = {
        "username": user.username,
        "session_id":user.session_id,
        "scopes": scopes
    }

    # Encode it
    refresh_token = jwt.encode(
        refresh_data,
        config.settings.secret,
        "HS256"
    )

    # Return
    return global_classes.TokenPair(
        access_token = access_token,
        refresh_token=refresh_token
    )
    
# Retrieve the global_classes from utilities
from ..utilities import global_classes

# Get database utilities
from .. import database

# Get permissions information
from . import permissions

# Hashlib for password hashing
import hashlib

# Jose for JWT
from jose import jwt

# Calendar and datetime for time stuff
import calendar
from datetime import datetime, time, timedelta

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

def issue_token_pair(user: global_classes.User, ttl: int = 30, scopes: list[str] = permissions.default_permissions):
    """
        Issues an access/refresh token pair.
    """

    # Expires time
    exp_time = datetime.utcnow()+timedelta(minutes=ttl)

    # Dictionary containing data for access token
    access_data = {
        "username":user.username,
        "expires": calendar.timegm(exp_time.timetuple())
    }
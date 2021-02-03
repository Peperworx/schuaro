# Retrieve the global_classes from utilities
from schuaro.users.authcode import login
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
from jose import jwt, JWTError

# Secrets for random codes
import secrets

# Calendar and datetime for time stuff
import calendar
from datetime import datetime, time, timedelta

# Base64 stuff
import base64

# Http error
from fastapi import HTTPException, status

async def verify_user(username: str, password: str) -> global_classes.UserDB:
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
    db = await database.get_db()


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
    

    # Return the user
    return user

async def issue_token_pair(user: global_classes.UserDB, ttl: int = 30, scopes: list[str] = permissions.default_permissions) -> Optional[global_classes.TokenPair]:
    """
        Issues an access/refresh token pair.
    """

    # Expires time
    exp_time = datetime.utcnow()+timedelta(minutes=ttl)

    # Dictionary containing data for access token
    access_data = {
        "domain":"access",
        "username":user.username,
        "tag":user.tag,
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
        "domain":"refresh",
        "username": user.username,
        "tag":user.tag,
        "session_id":user.session_id,
        "scopes": scopes
    }

    # Encode it
    refresh_token = jwt.encode(
        refresh_data,
        config.settings.secret,
        "HS256"
    )

    # Validate the access token
    access_token_valid = await validate_access_token(global_classes.AccessToken(**access_data))

    # If access token is not valid, fail
    if not access_token_valid:
        return None

    # Return
    return global_classes.TokenPair(
        access_token = access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


async def validate_access_token(token: global_classes.AccessToken) -> bool:
    """
        Validates an access token
    """

    # Validate expiry
    current_time = calendar.timegm(datetime.utcnow().timetuple())

    # If expires < current time, fail
    if token.expires < current_time:
        return False
    
    # Get user
    user = await get_user(token.username,token.tag)

    # If the user does not exist, fail
    if not user:
        return False

    # If the session_id does not match, fail
    if token.session_id != user.session_id:
        return False
    
    # Verify that the user has required scopes
    for scope in token.scopes:
        if scope not in user.permissions:
            return False

    # If all is good, return true
    return True
    

async def decode_access_token(token:str) -> Optional[global_classes.AccessToken]:
    """
        Decodes a token, returning none if it fails
    """
    try:
        decoded = jwt.decode(
            token,
            config.settings.secret,
            "HS256"
        )
    except JWTError:
        return None
    
    # Verify decoded
    tok = global_classes.AccessToken(
        **decoded
    )
    
    # Validate and fail if invalid
    if await validate_access_token(tok):
        return tok
    else:
        return None


async def get_user(username: str, tag: int) -> Optional[global_classes.UserDB]:
    """
        Returns a user with username and tag
    """

    # Retrive the database and the collection
    db = await database.get_db()
    col = db["schuaro-users"]

    # Get the user
    user = col.find_one(
        {
            "username":username,
            "tag":tag
        }
    )

    # If it is none, return
    if not user:
        return None
    
    # Else, return the pydantic model
    return global_classes.UserDB(
        **user
    )

async def validate_authcode(token: global_classes.AuthCode, code_verifier: Optional[str] = None) -> bool:
    """
        Validates an authcode.
    """

    # Validate expiry
    current_time = calendar.timegm(datetime.utcnow().timetuple())

    # If expires > current time, fail
    if token.expires < current_time:
        return False
    
    # Get user
    user = await get_user(token.username,token.tag)

    # If the user does not exist, fail
    if not user:
        return False

    # If the session_id does not match, fail
    if token.session_id != user.session_id:
        return False
    
    # Verify that the user has required scopes
    for scope in token.scopes:
        if scope not in user.permissions:
            return False

    # Are we verifying a code challenge?
    if not code_verifier:
        # If we are not, we are all good
        return True

    # If we are, verify

    # If the method is invalid, fail
    if token.code_challenge_method not in ["S256","plain"]:
        return False
    
    # Add back challenge padding
    padding = 4 - (len(token.code_challenge) % 4)
    token.code_challenge = token.code_challenge + ('=' * padding)
    

    # Decode the challenge
    challenge = base64.urlsafe_b64decode(token.code_challenge)
    
    # If it is sha256, hash and compare
    if token.code_challenge_method == "S256":
        # Get the hex of challenge
        challenge_hex = challenge.hex()

        # Hash the code
        code_hex = hashlib.sha256(code_verifier.encode()).hexdigest()

        # Return if they are equal
        return challenge_hex == code_hex
    
    # If not, compare
    else:
        return challenge == code_verifier

async def decode_authcode(token:str,code_verifer:str) -> Optional[global_classes.AuthCode]:
    """
        Decodes an authcode, returning none if fails
    """
    try:
        decoded = jwt.decode(
            token,
            config.settings.secret,
            "HS256"
        )
    except JWTError:
        return None
    
    # Verify decoded
    tok = global_classes.AuthCode(
        **decoded
    )
    
    # Validate and fail if invalid
    if await validate_authcode(tok,code_verifer):
        return tok
    else:
        return None

async def issue_authcode(
    user: global_classes.UserDB,
    login_request: global_classes.LoginRequest,
    ttl: int = 30,
    scopes: list[str] = permissions.default_permissions
    ) -> Optional[str]:
    """
        Issues an authorization code for using authcode login
    """
    expiry = datetime.utcnow()+timedelta(minutes=ttl)

    # Create data
    authcode_data = global_classes.AuthCode(
        username = user.username,
        tag = user.tag,
        scopes = scopes,
        expires = calendar.timegm(expiry.timetuple()),
        session_id = user.session_id,
        redirect_uri = login_request.redirect_uri,
        code_challenge = login_request.code_challenge,
        code_challenge_method = login_request.code_challenge_method
    )

    # Validate
    validated = await validate_authcode(authcode_data)

    # If not validated, fail
    if not validated:
        return None

    # Encode authcode
    authcode = jwt.encode(
        authcode_data.dict(),
        config.settings.secret,
        "HS256"
    )

    # Return
    return authcode
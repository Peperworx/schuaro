"""
    Authcode handlers for OAuth2
"""

# Data representations
from schuaro.errors import AuthcodeError
from schuaro.data import rep

# Database stuff
import schuaro.data as data

# Utilities
import schuaro.utilities as util

# Clients
from schuaro import clients as client_utils

# Users
from schuaro.users import utils as user_utils

# jose for JWT
from jose import jwt, JWTError

# Calendar and datetime for time stuff
import calendar
from datetime import datetime, time, timedelta

# Optional types
from typing import Optional

# Base64 and Hashlib
import base64
import hashlib

# Fastapi
from fastapi import Request

# Configuration
from schuaro import config

async def validate_authcode(token: rep.AuthCode, code_verifier: Optional[str] = None):
    """
        Validates an authcode.
    """

    # Validate expiry
    current_time = calendar.timegm(datetime.utcnow().timetuple())

    # If expires > current time, fail
    if token.expires < current_time:
        raise AuthcodeError("Authcode Expired")
    
    # Get user
    user = await data.find_user_email(token.email)

    # If the session_id does not match, fail
    if token.session_id != user.session_id:
        raise AuthcodeError("Session ID does not match")
    
    # Verify that the user has required scopes
    for scope in token.scopes:
        if scope not in user.permissions:
            raise AuthcodeError("Unexpected scopes")

    # Are we verifying a code challenge?
    if not code_verifier:
        # If we are not, we are all good
        return True
    
    # If we are, verify

    # If the method is invalid, fail
    if token.code_challenge_method not in ["S256","plain"]:
        raise AuthcodeError("Incorrect challeng type")
    
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
        if challenge_hex == code_hex:
            return True
        else:
            raise AuthcodeError("Challenge Failed")
    
    # If not, compare
    else:
        if challenge == code_verifier:
            return True
        else:
            raise AuthcodeError("Challenge Failed")


async def create_authcode(
    user: rep.DB_User, 
    login_request: rep.LoginRequest,
    ttl: int,
    scopes: list[str]):
    """
        Creates and returns an authcode
    """

    # Calculate expiry
    expiry = datetime.utcnow()+timedelta(minutes=ttl)

    # Create Dataclass
    authcode_data = rep.AuthCode(
        username = user.username,
        email = user.email,
        tag = user.tag,
        scopes = scopes,
        expires = calendar.timegm(expiry.timetuple()),
        session_id = user.session_id,
        redirect_uri = login_request.redirect_uri,
        code_challenge = login_request.code_challenge,
        code_challenge_method = login_request.code_challenge_method
    )

    # Validate the authcode
    validated = await validate_authcode(authcode_data)

    # Encode the authcode
    authcode = jwt.encode(
        authcode_data.dict(),
        config.settings.secret,
        "HS256"
    )

    # Return
    return authcode

async def authenticate(login_request: rep.LoginRequest):
    """
        Generates an authcode authentication token
    """

    # Parse the scopes
    scopes = util.parse_scopes(login_request.scope)

    # Retrieve the client
    client = await data.find_client(login_request.client_id)

    # Verify the client
    clientv = await client_utils.verify_client_scopes(client, scopes)

    # Retrieve the user
    user = await data.find_user_email(login_request.username)
    
    # Verify the user
    userv = await user_utils.verify_user(user, login_request.password, scopes)



    # Issue the authcode
    ttl = 30
    authcode = await create_authcode(
        user,
        login_request,
        ttl,
        scopes
    )

    

    # Return
    return authcode

async def password(token_request: rep.OAuthTokenRequest, request: Request) -> rep.TokenResponse:
    """
        Grant for password login.
    """
    pass
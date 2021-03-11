"""
    Authcode handlers for OAuth2
"""

# Data representations
from schuaro.data import rep

# Errors
from schuaro.errors import AuthcodeError, ClientInvalid
from fastapi import HTTPException, status

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

async def validate_authcode(token: rep.AuthCode, code_verifier: Optional[str] = None) -> bool:
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
    scopes: list[str]) -> str:
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

async def authenticate(login_request: rep.LoginRequest) -> str:
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

async def extract_client(token_request: rep.OAuthTokenRequest, request: Request) -> rep.ClientAuthenticatio:
    """
        Extracts the details of the client from both the request and the headers.
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
        raise ClientInvalid("Client Not Found in Request")
    
    if not client_id or not client_secret:
        raise ClientInvalid("Client Not Found in Request")

    # If it exists, we will have reached this point
    # Lets create the return structure and return
    return rep.ClientAuthentication(
        client_id=client_id,
        client_secret=client_secret
    )

async def authorization_code(token_request: rep.OAuthTokenRequest, request: Request) -> rep.TokenResponse:
    """
        Grant for OAuth2 Authorization Code login.
    """
    try:
        # Retrieve details of the client
        client_details = await extract_client(token_request,request)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no_client_details",
            headers={
                "WWW-Authenticate": f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    

    # Retrive scope details
    scopes = util.get_scopes(token_request.scopes)
    
    
    # Get the client
    client = data.find_client(client_details.client_id)

    # Verify the client
    try:
        await client_utils.verify_client(client, client_details.client_secret, scopes)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="client_credentials_incorrect",
            headers={
                "WWW-Authenticate": f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
            }
        )
    
    
    
    # NOTE Any clients can authorize users
    
    # NOTE Above validation already checks scopes
    
    # Decode the authcode
    authcode = await decode_authcode(token_request.code,token_request.code_verifier)
    
    # Check if authcode is valid, failing if not
    if not authcode:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="authcode_invalid",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
        )
    
    # Verify the authcodes redirect_uri
    if authcode.redirect_uri != token_request.redirect_uri:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="authcode_invalid_redirect",
                headers={
                    "WWW-Authenticate":
                        f"Bearer{f' scope={token_request.scope}' if len(scopes) > 0 else ''}"
                }
        )

    # Now we know the authcode is valid.

    
    # Timetolive of 30 mins
    ttl = 30

    # Lets issue a token
    issued_tokens = await user_utils.issue_token_pair(
        await user_utils.get_user(
            authcode.username,
            authcode.tag
        ),
        ttl=ttl,
        scopes=authcode.scopes
    )
    
    # Generate the response
    ret = {
        "token_type":"bearer",
        "expires":ttl*60, # How many seconds till expiry
        "access_token":issued_tokens.access_token,
        "scope": " ".join(scopes), # The scopes
        "refresh_token":issued_tokens.refresh_token # The refresh token
    }
    
    # Load into model and return
    return rep.TokenResponse(**ret)
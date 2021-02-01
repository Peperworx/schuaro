# Retrieve the global_classes from utilities
from os import access
from ..utilities import global_classes

# Get database utilities
from .. import database

# Get permissions information
from . import permissions

# Get configuration data
from .. import config

# Hashlib for password hashing
import hashlib

# jwcrypto for tokens and keys
from jwcrypto import jwk, jwt

# JSON for loading keys
import json

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

def issue_token_pair(user: global_classes.User, ttl: int = 30, scopes: list[str] = permissions.default_permissions) -> global_classes.TokenPair:
    """
        Issues an access/refresh token pair.
    """

    # Expires time
    exp_time = datetime.utcnow()+timedelta(minutes=ttl)

    # Dictionary containing data for access token
    access_data = {
        "username":user.username,
        "expires": calendar.timegm(exp_time.timetuple()),
        "scopes":scopes
    }
    
    # Load the key for access tokens
    access_key  =  jwk.JWK.from_json(config.settings.access_token_key)

    # Load the key for refresh tokens
    refresh_key = jwk.JWK.from_json(config.settings.refresh_token_key)
    
    # Generate the access token
    access_token_signed = jwt.JWT(
        header={"alg":"RS512"},
        claims=access_data
    )

    # Sign the access token
    access_token_signed.make_signed_token(key=access_key)

    # Dump it
    signed_access = access_token_signed.serialize()

    # Generate encrypted access tokens
    access_token_encrypted = jwt.JWT(
        header={
            "alg":"RSA-OAEP-256",
            "enc": "A256BC-HS512"
        },
        claims = signed_access
    )

    # Encrypt the access token
    access_token_encrypted.make_encrypted_token(access_key)

    # Dump the access token
    access_token = access_token_encrypted.serialize()


    # We now have the access token

    # Now we need to create the refresh token

    # Refresh token contains a sha256 hash of the signed access token, 
    # a sha256 hash of the encrypted token, and a sha256 of the expiry date
    # as well as the username

    refresh_data = {
        "username": access_data["username"],
        # The signed hash
        "signed": hashlib.sha256(signed_access).hexdigest().lower(),
        # The encrypted hash
        "encrypted": hashlib.sha256(access_token).hexdigest().lower(),
        # And finally, the expiry
        "expires": hashlib.sha256(access_data["expires"]).hexdigest().lower()
    }

    # This uses symmetric cryptography as opposed to asymmetric

    # Create a signed token
    refresh_token_signed = jwt.JWT(
        header={
            "alg":"HS256"
        },
        claims = refresh_data
    )

    # Sign it
    refresh_token_signed.make_signed_token(refresh_key)

    # Create an encrypted token
    refresh_token_encrypted = jwt.JWT(
        header={
            "alg":"A256KW",
            "enc": "A256BC-HS512"
        },
        claims = refresh_token_signed.serialize()
    )

    # Encrypt it
    refresh_token_encrypted.make_encrypted_token(refresh_key)

    # Dump it
    refresh_token = refresh_token_encrypted.serialize()
    
    # Return keypair
    return global_classes.TokenPair(
        access_token=access_token,
        refresh_token=refresh_token
    )
    
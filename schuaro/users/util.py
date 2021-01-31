from typing import Optional
from pydantic import BaseModel

# Import configuration details
from .. import config

# Import database stuff
from . import db

# Global Types
from . import glob

# Jose for JWT
from jose import jwt

# Regex for username validation
import re

# Datetime stuff
from datetime import timedelta, datetime
import calendar
import time



def parse_username(username):
    """
        Parses a username into a username and a tag
    """

    # Split the string by hashtag
    u_split = username.split("#")

    # Now we confirm that the length is EQUAl to two
    if not len(u_split) == 2:
        return glob.ParsedUsername(success=False,username="",tag=0)
    
    # Now that we know the length is equal to two
    # lets make sure that the username matches our validation regex.
    u_match = re.match(r"[a-zA-Z_\-][a-zA-Z0-9_\-]*",u_split[0])

    # If it matches, set the username
    if u_match:
        username = u_split[0]
    else: # If not, return error
        return glob.ParsedUsername(success=False,username="",tag=0)
    
    # Now lets make sure the tag matches
    # Confirm that it is in fact a hexidecimal numeric string
    if not re.match(r"[0-9a-fA-F]+",u_split[1]):
        return glob.ParsedUsername(success=False,username=username,tag=0)

    # If it succeded, convert to integer and return
    tag = int(u_split[1],16)

    return glob.ParsedUsername(
        success=True,
        username=username,
        tag=tag
    )

def generate_token(user,ttl:int=30,scopes:list['str']=[]) -> glob.Token:


    # Initialize Token Data class
    to_enc = glob.TokenData()


    # Generate expires time
    exp_time = datetime.utcnow() + timedelta(minutes=ttl)

    # Set the token expiration time
    to_enc.expires = calendar.timegm(exp_time.timetuple())

    # Set token's username
    to_enc.username = user.username

    # And the tag
    to_enc.tag = user.tag

    
    

    # Encode the token
    token = jwt.encode(
        dict(to_enc),
        config.settings.secret,
        algorithm = "HS256"
    )

    # Create the token class
    to_ret = glob.Token(
        access_token=token,
        token_type="bearer"
    )

    # Return
    return to_ret



def decode_token(token:str) -> glob.TokenData:
    try:
        dec = glob.TokenData(**jwt.decode(
            token,
            config.settings.secret
        ))
        # Verify time
        now = int(calendar.timegm(datetime.now().timetuple()))
        if dec.expires < now:
            return None
        return dec
    except:
        return None



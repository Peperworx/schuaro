from typing import Optional
from pydantic import BaseModel
from fastapi import Depends
import hashlib
from . import glob

# Import utilities
from . import util

fake_db = [
    {
        "username":"test",
        "tag":0x8188,
        "password":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
        "active":True,
        "public":True,
        "permissions":[
            "me",
            "user:read",
            "ability:friends",
            "ability:party",
            "ability:match_request"
        ]
    }
]






def get_user_mock(user: glob.ParsedUsername) -> Optional[glob.User]:
    """
        Retrieves a fake user from the fake database
    """
    for u in fake_db:
        # Load user
        u_load = glob.User(**u)

        # Check username and tag
        if u_load.tag == user.tag and u_load.username == user.username:
            return u_load
    
    return None


def get_user(user: glob.ParsedUsername) -> Optional[glob.User]:
    """
        Retrieves a user from username and tag
    """

    return get_user_mock(user)


def verify_user(user: glob.ParsedUsername, password: str, scopes: list[str]) -> Optional[glob.User]:
    """
        Verify the user and returns.
        If the user is valid, returns the user.
        If not, returns None
    """

    # Retrieve the user
    ret_user = get_user(user)

    # Check if it is valid
    if ret_user == None:
        return None
    
    # Check password
    if hashlib.sha256(password.encode()).hexdigest() != ret_user.password:
        return None
    
    for scope in scopes:
        if scope not in ret_user.permissions:
            return None

    # Return
    return ret_user


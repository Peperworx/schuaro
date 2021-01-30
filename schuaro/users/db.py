from typing import Optional
from pydantic import BaseModel
from fastapi import Depends


# Import utilities
from . import util

fake_db = [
    {
        "username":"test",
        "tag":0x8188,
        "password":"test"
    }
]






def get_user_mock(user: util.ParsedUsername) -> Optional[User]:
    """
        Retrieves a fake user from the fake database
    """
    for u in fake_db:
        # Load user
        u_load = User(**u)

        # Check username and tag
        if u_load.tag == user.tag and u_load.username == user.username:
            return u_load
    
    return None


def get_user(user: util.ParsedUsername) -> Optional[User]:
    """
        Retrieves a user from username and tag
    """

    return get_user_mock(user)


def verify_user(user: util.ParsedUsername, password: str) -> Optional[User]:
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
    if password != ret_user.password:
        return None

    # Return
    return ret_user


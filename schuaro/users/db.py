from typing import Optional
import hashlib
from . import glob
from .. import config
from pymongo import MongoClient

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
            "ability:match_request",
            "ability:chat"
        ]
    }
]



async def get_db():
    client = MongoClient(
        config.settings.mongo_host,
        config.settings.mongo_port
    )
    
    # Grab the DB
    db = client[config.settings.db_name]
    
    # Return the DB
    return db


async def get_user_mongo(user: glob.ParsedUsername) -> Optional[glob.User]:
    db = await get_db()
    
    # Grab the collection
    col = db["schuaro-users"]
    
    # Find the user
    u = col.find_one(
        {
            "username":user.username,
            "tag":user.tag
        }
    )

    # If it does not exist, return none
    if not u:
        return None
    
    # If it does, return it as a user
    return glob.User(**u)
    



async def get_user_mock(user: glob.ParsedUsername) -> Optional[glob.User]:
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


async def get_user(user: glob.ParsedUsername) -> Optional[glob.User]:
    """
        Retrieves a user from username and tag
    """

    return await get_user_mongo(user)


async def verify_user(user: glob.ParsedUsername, password: str, scopes: list[str]) -> Optional[glob.User]:
    """
        Verify the user and returns.
        If the user is valid, returns the user.
        If not, returns None
    """

    # Retrieve the user
    ret_user = await get_user(user)

    # Check if it is valid
    if ret_user == None:
        return None
    
    # Check password
    if hashlib.sha256(password.encode()).hexdigest().lower() != ret_user.password.lower():
        return None
    
    for scope in scopes:
        if scope not in ret_user.permissions:
            return None

    # Return
    return ret_user


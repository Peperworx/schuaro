from re import L
from typing import Optional
import hashlib
from . import glob
from .. import config
from pymongo import MongoClient
import secrets

# Import utilities
from . import util

# Import permissions
from . import permissions


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
            "username":user.username.lower(),
            "tag":user.tag
        }
    )

    # If it does not exist, return none
    if not u:
        return None
    
    # If it does, return it as a user
    return glob.User(**u)
    

async def get_reserved_mongo() -> list[glob.ReservedReason]:
    """
        Returns a list of reserved prefixes and suffixes from mongodb.
    """

    db = await get_db()

    col = db["schuaro-reserved"]
    

    return [glob.Reserved(**c) for c in col.find()]

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


async def create_user(
    user: glob.ParsedUsername, 
    password: str, 
    perms: list[str] = permissions.default_permissions
    ) -> Optional[glob.UserCreateErrors]:
    """
        Created a user, excluding reserved prefixes and suffixes.
    """

    # Retrieve all reserved pre/suffixes
    resed = await get_reserved_mongo()
    # Check name
    for res in resed:
        # If it starts with, endswith, or is a reserved name, fail
        if user.username.lower() == res.reserved:
            return glob.UserCreateErrors.RESERVED_NAME
        elif user.username.lower().startswith(res.reserved):
            return glob.UserCreateErrors.RESERVED_PREFIX
        elif user.username.lower().endswith(res.reserved):
            return glob.UserCreateErrors.RESERVED_SUFFIX
        
    
    # If we are here, we can go ahead and create
    # Grab the db
    db = await get_db()

    # And the collection
    col = db["schuaro-users"]

    # Generate the user
    u = glob.User(**{
        "username":user.username.lower(),  # Lowercaseify username
        "tag": user.tag,
        "password":hashlib.sha256(password.encode()).hexdigest().lower(),
        "active": True,
        "public": True,
        "permissions": perms
    })

    # And add
    insed = col.insert_one(
        dict(u)
    )

    # Return no error
    return glob.UserCreateErrors.NO_ERROR


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

async def generate_client(perms = permissions.default_clients) -> glob.Client:
    """
        Generates a random clientid and secret
    """

    # Generate initial clientid
    client_id = hex(secrets.randbits(256))[2:]
    
    # Grab the db and collection
    db = await get_db()
    col = db["schuaro-clients"]

    # Modify clientid until it does not exist in db
    while col.find_one({"client_id":client_id}):
        client_id = hex(secrets.randbits(256))[2:]
    
    # Generate the client secret
    client_secret = hex(secrets.randbits(256))[2:]

    # Load into class
    client = glob.Client(
        client_id = client_id,
        client_secret = hashlib.sha256(client_secret.encode()).hexdigest(), # Hash the client secret
        permissions=perms
    )

    # Insert into database
    col.insert_one(dict(client))

    # We want to return the actual secret
    client.client_secret = client_secret    

    # Return
    return client

async def get_client(client_id: str) -> glob.Client:
    # Get db and collection
    db = await get_db()
    col = db["schuaro-clients"]


    # Find it
    client = col.find_one(
        {
            "client_id": client_id
        }
    )

    # Return it
    return glob.Client(**client)

async def validate_client(client_id: str, client_secret: str) -> Optional[glob.Client]:
    """
        Validates a client.
    """

    # If either is none, fail
    if None in [client_id,client_secret]:
        return None
    
    # Grab the client
    client = await get_client(client_id)


    # If it was not found, fail
    if not client:
        return None
    

    # Check the secret, and if it does not match, fail
    if hashlib.sha256(client_secret.encode()).hexdigest().lower() != client.client_secret.lower():
        return None
    
    # Return the client
    return client
    


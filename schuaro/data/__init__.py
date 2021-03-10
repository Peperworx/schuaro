"""
    Database functions for schuaro
"""
# Pymongo
import pymongo

# Pymongo database
import pymongo.database

# Grab config
from schuaro import config

# And the data structures
from schuaro.data import rep

# Errors
from schuaro.errors import *





async def get_db() -> pymongo.database.Database:
    """
        Retrieves the mongodb database
    """

    # Get the client
    cli = pymongo.MongoClient(config.settings.mongo_connstring)

    # return the database
    return cli[config.settings.db_name]


async def find_user_email(email) -> rep.DB_User:
    """
        Retrieves a user from the database based off of their email
    """

    # Grab the database
    db = await get_db()

    # We want the users collection
    users_collection = f"{config.settings.col_prefix}-users"

    # Grab the collection
    col = db[users_collection]

    # Find the user
    user = col.find_one({"email":email})

    # If the user does not exist, raise error
    # If it does, return user
    if user:
        return rep.DB_User(**user)
    else:
        raise UserNotFound(f"Unable to find user with email {email}")

async def find_client(client_id: str):
    """
        Retrieves a client from the database based off of ID
    """

    # Grab the database
    db = await get_db()

    # We want the clients collection
    clients_collection = f"{config.settings.col_prefix}-clients"

    # Grab the collection
    col = db[clients_collection]

    # Find the client
    client = col.find_one({"client_id":client_id})

    # If the user does not exist, raise error
    # If it does, return user
    if client:
        return rep.DB_Client(**client)
    else:
        raise ClientNotFound(f"Unable to find client with id {client_id}")
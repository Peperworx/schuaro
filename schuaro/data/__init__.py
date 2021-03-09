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
    users_collection = f"{config.settings.col_prefix}_users"

    # Grab the collection
    col = db[users_collection]

    # Find the user
    user = col.find_one({"email":email})

    # If the user does not exist, raise error
    # If it does, return user
    if user:
        return user
    else:
        raise UserNotFound(f"Unable to find user with email {email}")


def noasync_get_db() -> pymongo.database.Database:
    """
        Retrieves the mongodb database
    """

    # Get the client
    cli = pymongo.MongoClient(config.settings.mongo_connstring)

    # return the database
    return cli[config.settings.db_name]


def noasync_find_user_email(email) -> rep.DB_User:
    """
        Retrieves a user from the database based off of their email
    """
    
    # Grab the database
    db = noasync_get_db()
    
    # We want the users collection
    users_collection = f"{config.settings.col_prefix}_users"

    # Grab the collection
    col = db[users_collection]

    # Find the user
    user = col.find_one({"email":email})

    # Return the users
    return user
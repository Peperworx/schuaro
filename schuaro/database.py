from .utilities import global_classes
from .config import settings
import pymongo

def get_db():
    """
        Retrieves a pymongo database instance based off of current configuration data.
    """
    # Create Mongo instance
    cli = pymongo.MongoClient(
        settings.mongo_host,
        settings.mongo_port
    )

    # Grab DB
    db = cli[settings.db_name]

    # Return
    return db




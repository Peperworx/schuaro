from schuaro.utilities import global_classes
from schuaro.config import settings
import pymongo

async def get_db():
    """
        Retrieves a pymongo database instance based off of current configuration data.
    """
    # Create Mongo instance
    cli = pymongo.MongoClient(
        settings.mongo_connstring
    )

    # Grab DB
    db = cli[settings.db_name]

    # Return
    return db




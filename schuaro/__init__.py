# Grab FastAPI class
from schuaro.error import ConfigurationInvalidError
from fastapi import FastAPI

# Schuaro imports
from schuaro import config
from schuaro.data import redis as dredis

# Redis
import redis

# Socket for hostname discovery
import socket



# Metadata for tags
tags_metadata = [
]


# Initialize the app
app = FastAPI(
    swagger_ui_init_oauth = {
        "usePkceWithAuthorizationCodeGrant":True
    },
    openapi_tags = tags_metadata
)

@app.on_event("startup")
async def startup():
    """
        Prepare the application
    """

    # Get the local configuration
    conf = config.read_local_configuration()

    # Attempt to connect to redis
    try:
        rpool = redis.ConnectionPool(
            host=conf["redis_host"],
            port=conf["redis_port"],
        )
        # Create a dummy connection
        r = await dredis.try_connect(
            host=conf["redis_host"],
            port=conf["redis_port"],
            connection_pool=rpool)
    except IndexError as e:
        raise ConfigurationInvalidError("Configuration file missing one key of {redis_host, redis_port}")
    

    
# Grab FastAPI class
from schuaro.error import ConfigurationInvalidError
from fastapi import FastAPI

# Schuaro imports
from schuaro import config


# Redis
import redis

# Secrets
import secrets
import hashlib

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
        #r = redis.Redis(connection_pool=rpool)

        # Generate two random values
        ra = hashlib.sha256(secrets.randbits(2048).to_bytes(256,"little")).hexdigest()
        rb = hashlib.sha256(secrets.randbits(2048).to_bytes(256,"little")).hexdigest()
        # Attempt to set ker ra to value rb
        #r.set(ra,rb)

        # Try to get it
        #rg = r.get(ra)

        # And delete it
        #r.delete(ra)
    except IndexError as e:
        raise ConfigurationInvalidError("Configuration file missing one key of {redis_host, redis_port}")
    except redis.exceptions.ConnectionError:
        raise ConfigurationInvalidError(f"Unable to connect to redis at address {conf['redis_host']}:{conf['redis_port']}")
    

    
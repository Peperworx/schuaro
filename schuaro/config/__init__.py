import pydantic
from pydantic import (
    RedisDsn,
    AnyUrl
)
import databases

from schuaro.data import redis as dredis
from schuaro.data.database import *




class ConfigSchema(pydantic.BaseModel):
    """
        This defines the configuration file schema
    """
    # Defines the target schuaro version (major,minor,patch)
    version: tuple[int,int,int] = (0,0,1)

    # Redis host
    redis_url: RedisDsn

    # Database URI. Can be mysql, sqlite, postgresql
    database_uri: str

class ConfigLoader:
    """
        Loads configuration, tests values, creates connections and required instances.
    """
        
    
    async def from_dict(self, config: dict):
        """
            Loads configuration, tests values, creates connections and required instances.

            arguments:
            - {config}: The configuration dictionary.
        """
        
        # Validate configuration
        self.config = ConfigSchema(**config)

    async def connect_redis(self):
        """
            Connects to redis and returns a redis connection object.
        """
        # Try Connect to redis
        redis = await dredis.try_connect(
            self.config.redis_url.host,
            self.config.redis_url.port,
        )

        # Return
        return redis

    
    async def retrieve_db(self):
        """
            Returns a DbManager instance.
        """

        # Create database manager
        database = databases.Database(str(self.config.database_uri))
        db = DbManager(database)

        # Attempt connect/disconnect
        await database.connect()
        await database.disconnect()

        # Return
        return db


    
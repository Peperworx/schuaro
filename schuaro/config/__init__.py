import pydantic
import enum
from pydantic import (
    RedisDsn,
    AnyUrl
)

from schuaro.data import redis as dredis




class ConfigSchema(pydantic.BaseModel):
    """
        This defines the configuration file schema
    """
    # Defines the target schuaro version (major,minor,patch)
    version: tuple[int,int,int] = (0,0,1)

    # Redis host
    redis_url: RedisDsn

    # Database URI. Can be mysql, sqlite, postgresql
    database_uri: AnyUrl

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

        # Try Connect to redis
        self.redis = await dredis.try_connect(
            self.config.redis_url.host,
            self.config.redis_url.port,
        )

        # Try Connect to database
        print(self.config)

    
# Redis
import redis
import redis.exceptions

# Typing stuff
from typing import Optional

# time
import time

# Errors
import schuaro.error

async def try_connect(host: str = "localhost" , port: int = 6379, password: Optional[str] = None, db: int = 0, connection_pool: Optional[redis.ConnectionPool] = None, count: int = 10, delay: int = 2):
    """
        Connects to redis instance {host}:{port} with password {password} db {db} and pool {connection_pool}
        If connection fails, retries {count} times waiting {delay} seconds between each attempt
    """

    r = redis.Redis(
        host=host, 
        port = port, 
        password = password, 
        db = db,
        connection_pool=connection_pool
    )

    while count > 0:
        
        # Attempt to send
        try:
            r.publish("testpub","none")
            return r
        except redis.exceptions.ConnectionError:
            time.sleep(delay)
            count -= 1
    
    if count == 0:
        raise schuaro.error.ConnectionError(f"Unable to connect to redis instance at {host}:{port}. Check instance status and verify configuration data.")
    
    
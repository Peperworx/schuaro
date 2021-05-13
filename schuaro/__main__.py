import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from schuaro import app

c = Config()
c.quic_bind = ["localhost:4433"]
asyncio.run(serve(app, Config()))
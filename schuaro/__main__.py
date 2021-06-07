import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from schuaro import app
import os

c = Config.from_toml("./config/hypercorn.toml")
asyncio.run(serve(app, c))
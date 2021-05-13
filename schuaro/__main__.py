import trio
from hypercorn.config import Config
from hypercorn.trio import serve

from schuaro import app
import os

c = Config.from_toml("./config/hypercorn.toml")
trio.run(serve, app, c)
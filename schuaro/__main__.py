import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from schuaro import app
import os

c = Config()
c.certfile = os.path.join(os.getcwd(),"certificate.pem")
c.keyfile = os.path.join(os.getcwd(),"key.pem")
c.quic_bind = ["0.0.0.0:4433"]
c.bind = ["0.0.0.0:443"]
c.insecure_bind = ["0.0.0.0:80"]

asyncio.run(serve(app, c))
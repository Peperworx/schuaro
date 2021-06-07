from fastapi import FastAPI

from schuaro.config import ConfigLoader

import yaml

import os


app = FastAPI()




@app.on_event("startup")
async def startup():
    
    # Fetch application root
    app_root = os.path.join(os.path.dirname(__file__),"../../")
    
    # Open configuration file, and load configuration
    with open(os.path.join(app_root,"config/config.yml")) as f:
        config = ConfigLoader()
        await config.from_dict(yaml.load(f,Loader=yaml.loader.Loader))
    
    # Set config in app state
    app.state.config = config

    # Open redis connection and set it in app state
    app.state.redis = config.connect_redis()

    # Fetch database manager and set in app state
    app.state.db = config.retrieve_db()

    # Connect to database
    app.state.db.database.connect()

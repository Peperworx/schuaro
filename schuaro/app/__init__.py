from fastapi import FastAPI

from schuaro.config import ConfigLoader

import yaml

import os




app = FastAPI()


@app.on_event("startup")
async def startup():
    app_root = os.path.join(os.path.dirname(__file__),"../../")
    print(app_root)
    with open(os.path.join(app_root,"config/config.yml")) as f:
        config = ConfigLoader()
        await config.from_dict(yaml.load(f,Loader=yaml.loader.Loader))
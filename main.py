from fastapi import FastAPI


import schuaro.users
import schuaro.config


app = FastAPI()






app.include_router(
    schuaro.users.router
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

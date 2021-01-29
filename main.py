from fastapi import FastAPI


import schuaro.users


app = FastAPI()


# Add users
app.include_router(
    schuaro.users.router
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

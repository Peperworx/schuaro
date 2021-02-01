from fastapi import FastAPI


import schuaro.users
import schuaro.config

# Stuff for key generation
from jwcrypto import jwk


app = FastAPI()



# Generate the keypair for issuing access tokens
access_key = jwk.JWK.generate(kty="RSA", size=2048)
schuaro.config.settings.access_token_key = access_key.export()

# Generate the key for issuing refresh tokens
refresh_key = jwk.JWK.generate(kty="oct", size=256)
schuaro.config.settings.refresh_token_key = refresh_key.export()



app.include_router(
    schuaro.users.router
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

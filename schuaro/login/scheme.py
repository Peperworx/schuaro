
# FastAPI Security
from fastapi.security import (
    OAuth2AuthorizationCodeBearer
)

# Oauth2 Scheme
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"/login",
    tokenUrl=f"/login/oauth2",
    refreshUrl=f"/login/oauth2",
)
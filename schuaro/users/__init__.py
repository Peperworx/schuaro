from fastapi import APIRouter


router = APIRouter(prefix="/users")



@router.get("/{username}", tags=["users"])
async def index(username: str):
    """
        Retrieves the public information of a user.
        This includes but is not limited to:
        - Username (duh)
        - User ID
        - Public Stats
            - Level, KD, Leaderboard Placement
    """
    return {}

@router.get("/private", tags=["users"])
async def private(token: str):
    """
        Retrieves the private information of the current user.
        This includes chats, private stats, etc.
    """
    print(token)
    return {}


@router.post("/auth")
async def auth():
    """
        Authenticates the user based off of an username and password.

        Returns a token.
    """
    return {}
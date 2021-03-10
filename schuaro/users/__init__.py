"""
    Contains GraphQL queries for users
"""

# Strawberry
import strawberry
from strawberry.asgi import GraphQL

# Data representation
from schuaro.data import rep

# Database
from schuaro import data


@strawberry.experimental.pydantic.type(model=rep.DB_User, fields=[
    'username',
    'tag',
    'email',
    'active',
    'public'
])

class User:
    pass

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, token: str, email: str) -> User:

        # Get the user
        user = await data.find_user_email(email)

        # Return the user
        return User(**user.dict(exclude={"password","session_id","permissions"}))

schema = strawberry.Schema(query=Query)

router = GraphQL(schema)
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
    async def user(self, email: str) -> User:
        data = {
            "username":"test",
            "tag":0xF00D,
            "email":"admin@peperworx.com",
            "active":True,
            "public":True
        }
        return User(**data)

schema = strawberry.Schema(query=Query)

router = GraphQL(schema)
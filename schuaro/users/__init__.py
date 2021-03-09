"""
    Contains GraphQL queries for users
"""

# Graphene for graphql
from graphene import String, ObjectType, List

# FastAPI router
from fastapi import APIRouter

# Starlette graphql
from starlette.graphql import GraphQLApp


# Graphene pydantic
from graphene_pydantic import PydanticObjectType

# Get our pydantic models
from schuaro.data import rep

# And our database stuff
from schuaro import data

# Some errors
from graphql import GraphQLError
from schuaro.errors import *

class User(PydanticObjectType):
    class Meta:
        model = rep.User
        exclude_fields = ()

class Query(ObjectType):
    user = User()
    
    def resolve_user(self,info):
        """
            Resolves a user in the database
        """
        
        # Grab the user by email
        user = data.noasync_find_user_email("admin@peperworx.com")
        if user:
            return user
        else:
            raise GraphQLError("Unable to find user")
        # Convert and return the user
        



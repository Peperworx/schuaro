"""
    Pydantic data representations for schuaro
"""

# Pydantic
import pydantic


class DB_User(pydantic.BaseModel):
    """
        Represents a user inside of the database
    """

    # These are the username and the tag.
    # The full username is a combination of username and tag
    # where username#hexidecimal_tag
    # This system allows users to have the name they want,
    # and allows duplicate names without conflicts.
    username: str
    tag: int

    # Email is actually used to log in, instead of username/tag
    # This is easier to remember than username#tag
    email: str

    # This is the hash of a password. NEVER store plaintext
    password: str

    # The session ID is used to validate tokens. When a token is used,
    # we check the token's sessionid and the user's session id
    # If these do not match, we reject the token.
    # This allows users to invalidate other accounts. This is also 
    # re-randomized whenever a password reset request is sent.
    sesion_id: int


    # Permissions is a list of strings, each one representing a permission
    # in the format of domain:permission
    # This allows schuaro to lock specific users out of features such as 
    # the administrator dashboard and to allow specific users features that
    # some do not have.
    permissions: list[str]


    # The active boolean describes whether the user is active or not.
    # Non active users may not login until a password reset or an email
    # verification is sent
    active: bool

    # The public boolean dictates whether or not the user wants to be visible
    # to other users
    public: bool



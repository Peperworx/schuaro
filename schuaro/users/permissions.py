scopes = {
    "me": "Permission to access self data",
    "user:read":"Permission to read other public users",
    "ability:friends":"The ability to add and remove friends from self",
    "ability:party":"The ability to create and accept party invitations",
    "ability:match_request":"The ability to create matchmaking requests",
    "ability:chat":"The ability to chat with others. Can be muted.",
    "ability:issue_client":"The ability to issue clients",
    "ability:administrator":"Grants administrator permissions",
    "nono":"No one can have this permission. Specifically for testing."
}


default_permissions = [
    "me",
    "user:read",
    "ability:friends",
    "ability:party",
    "ability:match_request",
    "ability:chat"
]


developer_permissions = [
    "me",
    "user:read",
    "ability:friends",
    "ability:party",
    "ability:match_request",
    "ability:chat",
    "ability:issue_client",
    "ability:administrator"
]


scopes_clients = {
    "grant:user_defaults":"Permission to grant default permissions to users",
    "create:user":"Permission to create regular users",
    "create:developer":"Permission to create developer accounts",
    "overload:reserved":"Permission to overload reserved names",
    "issue:default":"Permission to issue tokens with default permissions",
    "issue:developer":"Permission to issue tokens with developer permissions",
    "ability:login":"Permission to login a user"
}

default_clients = [
    "grant:user_defaults",
    "create:user",
    "create:developer",
    "overload:reserved",
    "issue:default",
    "issue:developer",
    "ability:login"
]
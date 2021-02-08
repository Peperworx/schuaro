scopes = {
    "me": "Permission to access self data",
    "user:read":"Permission to read other public users",
    "ability:friends":"The ability to add and remove friends from self",
    "ability:party":"The ability to create and accept party invitations",
    "ability:match_request":"The ability to create matchmaking requests",
    "ability:chat":"The ability to chat with others. Can be muted.",
    "ability:issue_client":"The ability to issue clients",
    "ability:administrator":"Administrator permissions",
    "nono":"No one can have this permission. Specifically for testing.",
    "offline_access":"allow offline access",
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


issue_clients = {f"issue:{k}":f"The ability to issue {k}" for k,v in scopes.items()}

scopes_clients = {
    "login:password":"Allows password login. This should only be issued to schuaro itself",
    "login:authcode":"Allows authcode login"
} | issue_clients

# Just allow default issue all for now.
default_clients = issue_clients.keys()

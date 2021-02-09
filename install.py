import os
import sys
import time
import re
import secrets
print("Installing requirements")
os.system(f"{sys.executable} -m pip install -r requirements.txt -q -q -q")
    

from rich.prompt import Prompt, Confirm
from rich.console import Console
import hashlib
import pymongo

from schuaro.users import permissions

console = Console()


def request_mongodb():
    console.print("1. Connection String")
    console.print("2. Enter host and port manually")

    connection_method = Prompt.ask("Which of the above methods to you want to use to connect to mongodb?", choices=["1","2"])

    if connection_method == "1":
        connection_string = Prompt.ask("Please enter your mongodb connection string")
        with console.status("Trying to connect to mongodb"):
            server_info = None
            mongo_client = None
            try:
                mongo_client = pymongo.MongoClient(connection_string)
                server_info = mongo_client.server_info()
            except:
                console.print("[red]Unable to connect to mongodb[/red]")
        if server_info:
            console.print("[green]Successfully connected to mongodb[/green]")
            return mongo_client
        else:
            console.print("[red]Unable to connect to mongodb[/red]")
            request_mongodb()

    elif connection_method == "2":
        host = Prompt.ask("Please enter your mongodb host", default="localhost")
        port = Prompt.ask("Please enter your mongodb port", default="27017")
        while not port.isdecimal():
            print("[red]Please enter a valid port number[/red]")
            port = Prompt.ask("Please enter your mongodb port", default="27017")
        with console.status("Trying to connect to mongodb"):
            server_info = None
            mongo_client = None
            try:
                mongo_client = pymongo.MongoClient(host,int(port))
                server_info = mongo_client.server_info()
            except:
                console.print("[red]Unable to connect to mongodb[/red]")
        if server_info:
            console.print("[green]Successfully connected to mongodb[/green]")
            return mongo_client
        else:
            console.print("[red]Unable to connect to mongodb[/red]")
            request_mongodb()

# Request the mongodb connection
mongo = request_mongodb()

# Request the database name
database_name = Prompt.ask("Please enter the name for the database that schuaro will use", default="schuaro")

# Request the collection prefix
collection_prefix = Prompt.ask("Please enter the prefix for collections in the database", default="myschuaro")

confirm = True
database_exists = False
# Check if the database exists, and has collections in it
if database_name in mongo.list_database_names():
    database_exists = True
    if any([i.startswith(collection_prefix) for i in mongo[database_name].list_collection_names()]):
        confirm = Confirm.ask("[red]Warning[/red] That database already exists, and contains collections with the same prefix previously specified. Do you want to continue?")
    else:
        confirm = Confirm.ask("[blue]Notice[/blue] That database already exists, but there are no conflicts. Do you want to continue?")

# If the answer is no, exit
if not confirm:
    sys.exit()

# Get the database
db = mongo[database_name]

def prompt_user():
    username = Prompt.ask("Enter what you want your initial administrator username to be")

    if username.strip() == "":
        console.print("[red]Error[/red] username must be non empty")
        return prompt_user()

    tag = Prompt.ask("Enter your users tag. This is an hexidecimal string")
    m = re.match(r"[0-9A-Fa-f]+", tag)
    if m:
        pass
    else:
        console.print("[red]Error[/red] your tag must be a hexidecimal string")
        return prompt_user()
    
    password = Prompt.ask("Enter your new password", password=True)
    passwordc = Prompt.ask("Confirm your new password", password=True)

    if password != passwordc:
        console.print("[red]Error[/red] passwords do not match")
        return prompt_user()
    
    return username, password, int(tag,16)

# Prompt for username and password
u,p,t = prompt_user()


# Create the collection for a user
with console.status("Creating initial user"):
    col = db[f"{collection_prefix}-users"]

    # Remove all documents
    col.delete_many({})
    
    user = {
        "username":u,
        "tag": t,
        "password": hashlib.sha256(p.encode()).hexdigest(),
        "active": True,
        "public": True,
        "permissions":permissions.developer_permissions,
        "session_id": secrets.randbits(32)
    }
    col.insert_one(user)
    console.print("[green]Created user[/green]")
    


import os
import sys
import time
print("Installing requirements")
os.system(f"{sys.executable} -m pip install -r requirements.txt -q -q -q")
    

from rich.prompt import Prompt
from rich.console import Console

import pymongo

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


database_name = Prompt.ask("Please enter the name for the database that schuaro will use", default="schuaro")
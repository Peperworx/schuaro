# Schuaro

Schuaro (pronounced sh-war-oh) is a video game server with a bevy of features.


The server is accessable using a REST API and a full-featured admin dashboard will be on it's way soon.


## Running the server

The server is designed using FastAPI. Uvicorn is the preferred ASGI server, and it can be run by executing the following command in Schuaro's root directory:

```bash
uvicorn main:app
```
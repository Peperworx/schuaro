# Schuaro

Schuaro (pronounced sh-war-oh) is a video game server designed for use internally with peperworx.


The server is accessable using a REST API and a full-featured admin dashboard will be on it's way soon.


## Running the server

The server is designed using FastAPI. Uvicorn is the preferred ASGI server, and it can be run by executing the following command in Schuaro's root directory:

```bash
uvicorn schuaro:app
```

Schuaro is being redesigned from the ground up to be horizontally scaled easily.
# Websockets exposer for the spacenav driver

This is a **work in progress** service that is supposed to make Onshape work with spacenav.

[FreeSpacenav/spacenavd](https://github.com/FreeSpacenav/spacenavd)

https://github.com/FreeSpacenav/spacenavd/issues/30

## Deploy

### Install deps

Docker and Docker Compose

### Self-signed certificates

You can import the nginx/certs/nginx-selfsigned.crt as a trusted cert or use your own - just replace the crt and key in nginx/certs.

### Run

```
docker-compose up
```

open https://127.51.68.120:8181/test and toggle your SpaceMouse.

The example https://3dconnexion.com/technical_support/web_threejs.html will also connect but will not move the piramid (since the WS payloads need to be figured out).

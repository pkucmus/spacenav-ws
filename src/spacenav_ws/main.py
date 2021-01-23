import asyncio
from pathlib import Path
import socket
from struct import unpack

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn

from spacenav_ws.event import from_message


BASE_DIR = Path(__file__).resolve().parent

origins = [
    "https://127.51.68.120",
    "https://127.51.68.120:8181",
    "https://3dconnexion.com",
    "https://cad.onshape.com",
]

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def get(request: Request):
    return templates.TemplateResponse("test_ws.html", {"request": request})


@app.route("/3dconnexion/nlproxy")
async def nlproxy(request):
    return JSONResponse({"port": "8181"})


@app.websocket("/")
@app.websocket("/3dconnexion")
async def websocket_endpoint(websocket: WebSocket):
    reader, __ = await asyncio.open_unix_connection("/var/run/spnav.sock")

    await websocket.accept(subprotocol="wamp")
    while True:
        chunk = await reader.read(32)
        message = from_message(unpack("iiiiiiii", chunk))
        print(message)
        await websocket.send_json(message.to_3dconn())


if __name__ == "__main__":
    uvicorn.run(
        "spacenav_ws.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
    )


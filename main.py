import socket
from struct import unpack
import asyncio

from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8181",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Spacenav websocket expose</title>
        <style>
            pre {display: inline;}
        </style>
    </head>
    <body>
        <h1>Spacenav websocket expose</h1>
        <div>motion: <pre id="motion">null</pre></div>
        <div>X: <pre id="X">null</pre></div>
        <div>Z: <pre id="Z">null</pre></div>
        <div>Y: <pre id="Y">null</pre></div>
        <div>pitch: <pre id="pitch">null</pre></div>
        <div>yaw: <pre id="yaw">null</pre></div>
        <div>roll: <pre id="roll">null</pre></div>
        <div>period: <pre id="period">null</pre></div>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8181/3dconnexion");
            var motion = document.getElementById('motion');
            var X = document.getElementById('X');
            var Z = document.getElementById('Z');
            var Y = document.getElementById('Y');
            var pitch = document.getElementById('pitch');
            var yaw = document.getElementById('yaw');
            var roll = document.getElementById('roll');
            var period = document.getElementById('period');
            console.log("I guess");
            ws.onmessage = function(event) {
                var data = JSON.parse(event.data);
                console.log(data);
                motion.textContent = data[0];
                X.textContent = data[1];
                Z.textContent = data[2];
                Y.textContent = data[3];
                pitch.textContent = data[4];
                yaw.textContent = data[5];
                roll.textContent = data[6];
                period.textContent = data[7];
            };
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.route("/3dconnexion/nlproxy")
async def nlproxy(request):
    return JSONResponse({"port": "8181"})


@app.websocket("/3dconnexion")
async def websocket_endpoint(websocket: WebSocket):
    reader, __ = await asyncio.open_unix_connection("/var/run/spnav.sock")

    await websocket.accept()
    while True:
        chunk = await reader.read(32)
        message = unpack("iiiiiiii", chunk)
        print(message)
        await websocket.send_json(message)


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

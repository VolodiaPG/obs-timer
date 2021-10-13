from collections import defaultdict
from json.decoder import JSONDecodeError
from typing import Any, Awaitable, Callable, List, Optional
from pathlib import Path
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi_utils.tasks import repeat_every
from starlette.responses import JSONResponse, Response
from events import AsyncEventBus, Event, EventBus
from fischer import game_clock
from fischer.game_clock import GameClock
from dataclasses import dataclass

app = FastAPI()
bus:EventBus = AsyncEventBus()

class ScoreUpdate(Event):
    pass

@dataclass
class WsConnect(Event):
    websocket: WebSocket
    channel: str

# html = Path('index.html').read_text()
game_clock = GameClock(counter=30, fischer=5)

class ScoreManager:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.p1 = 0
        self.p2 = 0
        bus.emit(ScoreUpdate())

    def get(self) -> dict[str, int]:
        return {"p1": self.p1, "p2": self.p2}

scores = ScoreManager()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        self.active_connections[channel].append(websocket)
        bus.emit(WsConnect(websocket=websocket, channel=channel))

    def disconnect(self, websocket: WebSocket, channel: str):
        self.active_connections[channel].remove(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, message: str, channel: str, origin: Optional[WebSocket] = None):
        for connection in self.active_connections.get(channel, []):
            if connection != origin:
                await connection.send_text(json.dumps(message))


manager = ConnectionManager()

async def process_actions(message: dict[str, Any], channel:str, manager: ConnectionManager, origin: WebSocket):
    print(message)
    if "action" not in message:
        return
    
    action = message["action"]
    if action == "NEXT":
        game_clock.next()
    elif action == "RESET":
        game_clock.init()
    elif action == "PAUSE":
        game_clock.interrupt()

async def process_scores(message: dict[str, Any], channel:str, manager: ConnectionManager, origin: WebSocket):
    print(message)
    if "p1" in message:
        scores.p1 += int(message["p1"])
    if "p2" in message:
        scores.p2 += int(message["p2"])
    bus.emit(ScoreUpdate())

async def process_default(message: dict[str, Any], channel:str, manager: ConnectionManager, origin: WebSocket):
    print(message)
    await manager.broadcast(message, channel, origin)

process_channels: dict[str, Callable[[dict[str, Any], str, ConnectionManager, WebSocket], Awaitable[None]]] = {
    "actions": process_actions,
    "scores": process_scores,
}

# @app.get("/")
# async def get():
#     return HTMLResponse(html)

@app.get("/new_game_clock/{turn_time}/{fischer_time}")
async def get(turn_time:int, fischer_time:int):
    global game_clock
    game_clock = GameClock(turn_time, fischer_time)

@app.post("/reset")
async def get():
    game_clock.init()
    scores.reset()
    bus.emit(ScoreUpdate())

@app.on_event("startup")
@repeat_every(seconds=0.2,raise_exceptions=True)
async def update_counter() -> None:
    data = {"p1": game_clock.timer1.get_counter(), "p2": game_clock.timer2.get_counter()}
    await manager.broadcast(data, "timer")

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            try:
                await process_channels.get(channel, process_default)(json.loads(data), channel, manager, websocket)
            except JSONDecodeError as err:
                print(err)

    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)

def score_update(_: ScoreUpdate) -> None:
    manager.broadcast(scores.get(), "scores")
    
bus.add_listener(ScoreUpdate, score_update)

def ws_connect(event: WsConnect) -> None:
    print(event.channel)
    # if event.channel == "scores":
    #     manager.send_personal_message(event.websocket, scores.get())

bus.add_listener(WsConnect, ws_connect)

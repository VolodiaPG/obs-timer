from collections import defaultdict
from json.decoder import JSONDecodeError
from typing import Any, Awaitable, Callable, Counter, List, Optional
from pathlib import Path
import json
import asyncio
from pydantic import BaseModel

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi_utils.tasks import repeat_every
from starlette.responses import JSONResponse, RedirectResponse, Response
from events import AsyncEventBus, Event, EventBus
from fischer import game_clock
from fischer.game_clock import GameClock
from dataclasses import dataclass
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

bus: EventBus = AsyncEventBus()


class ScoreUpdate(Event):
    pass

@dataclass
class ClockUpdate(Event):
    counter: int
    fischer: int


@dataclass
class WsConnect(Event):
    websocket: WebSocket
    channel: str


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

    async def send_personal_message(self, websocket: WebSocket, message: Any):
        await websocket.send_text(json.dumps(message))

    async def broadcast(
        self, message: Any, channel: str, origin: Optional[WebSocket] = None
    ):
        loop = asyncio.get_running_loop()
        for connection in self.active_connections.get(channel, []):
            if connection != origin:
                loop.create_task(connection.send_text(json.dumps(message)))


manager = ConnectionManager()


async def process_actions(
    message: dict[str, Any], channel: str, manager: ConnectionManager, origin: WebSocket
):
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


async def process_scores(
    message: dict[str, Any], channel: str, manager: ConnectionManager, origin: WebSocket
):
    print(message)
    if "p1" in message:
        scores.p1 += int(message["p1"])
    if "p2" in message:
        scores.p2 += int(message["p2"])
    bus.emit(ScoreUpdate())


async def process_default(
    message: dict[str, Any], channel: str, manager: ConnectionManager, origin: WebSocket
):
    print(message)
    await manager.broadcast(message, channel, origin)

async def process_clock(
    message: dict[str, Any], channel: str, manager: ConnectionManager, origin: WebSocket
):
    global game_clock
    game_clock = GameClock(message["counter"], message["fischer"])
    bus.emit(ClockUpdate(counter=message["counter"], fischer=message["fischer"]))

process_channels: dict[
    str, Callable[[dict[str, Any], str, ConnectionManager, WebSocket], Awaitable[None]]
] = {
    "actions": process_actions,
    "scores": process_scores,
    "clock": process_clock,
}


@app.post("/reset")
async def get():
    game_clock.init()
    scores.reset()
    bus.emit(ScoreUpdate())


@app.on_event("startup")
@repeat_every(seconds=0.2, raise_exceptions=True)
async def update_counter() -> None:
    data = {
        "p1": game_clock.timer1.get_counter(),
        "p2": game_clock.timer2.get_counter(),
        "active": {
            "p1": game_clock.active and game_clock.timer1.active,
            "p2": game_clock.active and game_clock.timer2.active,
        },
    }
    await manager.broadcast(data, "timer")


@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(websocket, channel)

    try:
        while True:
            data = await websocket.receive_text()
            try:
                await process_channels.get(channel, process_default)(
                    json.loads(data), channel, manager, websocket
                )
            except JSONDecodeError as err:
                print(err)

    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


async def score_update(_: ScoreUpdate) -> None:
    await manager.broadcast(scores.get(), "scores")


bus.add_listener(ScoreUpdate, score_update)


async def ws_connect(event: WsConnect) -> None:
    if event.channel == "scores":
        await manager.send_personal_message(event.websocket, scores.get())
        print(str(scores.get()))


bus.add_listener(WsConnect, ws_connect)

async def clock_update(event: ClockUpdate) -> None:
    await manager.broadcast({"counter": event.counter, "fischer": event.fischer }, "clock")


bus.add_listener(ClockUpdate, clock_update)

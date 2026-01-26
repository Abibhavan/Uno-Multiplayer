# websocket connection

from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, player_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[player_id] = websocket

    def disconnect(self, player_id: str):
        self.active_connections.pop(player_id, None)

    async def send(self, player_id: str, message: dict):
        if player_id in self.active_connections:
            await self.active_connections[player_id].send_json(message)

    async def broadcast(self, players: list, message: dict):
        for p in players:
            await self.send(p, message)

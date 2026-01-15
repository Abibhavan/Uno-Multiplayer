from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from room_manager import create_room, join_room, can_start_game
from pathlib import Path
import random
import string

app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/client/index.html")

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/client",
    StaticFiles(directory=BASE_DIR / "client"),
    name="client"
)

app.mount(
    "/libs",
    StaticFiles(directory=BASE_DIR / "libs"),
    name="libs"
)

connections = {}   # playerId -> websocket
player_rooms = {}  # playerId -> roomCode

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    player_id = ws.query_params.get("playerId")
    connections[player_id] = ws

    try:
        while True:
            data = await ws.receive_json()
            print(data)
            msg_type = data["type"]

            # --------------------
            # CREATE ROOM
            # --------------------
            if msg_type == "create_room":
                room_code = generate_room_code()
                room = create_room(room_code, player_id)
                player_rooms[player_id] = room_code

                await ws.send_json({
                    "type": "room_created",
                    "room": room
                })

            # --------------------
            # JOIN ROOM
            # --------------------
            elif msg_type == "join_room":
                room_code = data["room_code"]
                room = join_room(room_code, player_id)

                if not room:
                    await ws.send_json({
                        "type": "error",
                        "message": "Room not found"
                    })
                    continue

                player_rooms[player_id] = room_code

                # broadcast lobby update
                for pid in room["players"]:
                    await connections[pid].send_json({
                        "type": "lobby_update",
                        "room": room
                    })

            # --------------------
            # START GAME
            # --------------------
            elif msg_type == "start_game":
                room_code = player_rooms.get(player_id)
                room = join_room(room_code, player_id)

                if not can_start_game(room, player_id):
                    await ws.send_json({
                        "type": "error",
                        "message": "Only host can start with 2+ players"
                    })
                    continue

                for pid in room["players"]:
                    await connections[pid].send_json({
                        "type": "game_started"
                    })

    except WebSocketDisconnect:
        connections.pop(player_id, None)
        print(f"{player_id} disconnected")

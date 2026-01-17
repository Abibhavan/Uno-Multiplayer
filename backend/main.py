from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager
from room_manager import create_room, join_room, start_room, rooms
from game_logic import play_card, draw_card

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await manager.connect(player_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            # ---------- ROOM ----------
            if msg_type == "CREATE_ROOM":
                code = create_room(player_id)
                room = rooms[code]

                await manager.send(player_id, {
                    "type": "ROOM_UPDATE",
                    "room": {
                        "code": code,
                        "players": room["players"],
                        "host": room["host"]
                    }
                })

            elif msg_type == "JOIN_ROOM":
                code = data["room_code"]
                success = join_room(code, player_id)

                if not success:
                    await manager.send(player_id, {
                        "type": "ERROR",
                        "message": "Cannot join room"
                    })
                    continue

                room = rooms[code]
                await manager.broadcast(room["players"], {
                    "type": "ROOM_UPDATE",
                    "room": {
                        "code": code,
                        "players": room["players"],
                        "host": room["host"]
                    }
                })

            elif msg_type == "START_GAME":
                code = data["room_code"]
                state = start_room(code)
                players = rooms[code]["players"]

                await manager.broadcast(players, {
                    "type": "GAME_STATE",
                    "state": state
                })

            # ---------- GAME ----------
            elif msg_type == "PLAY_CARD":
                state = play_card(
                    data["room_code"],
                    player_id,
                    data["card"],
                    data.get("chosen_color")
                )

                if "error" in state:
                    await manager.send(player_id, {
                        "type": "ERROR",
                        "message": state["error"]
                    })
                    continue

                players = rooms[data["room_code"]]["players"]
                await manager.broadcast(players, {
                    "type": "GAME_STATE",
                    "state": state
                })

            elif msg_type == "DRAW_CARD":
                state = draw_card(data["room_code"], player_id)
                players = rooms[data["room_code"]]["players"]

                await manager.broadcast(players, {
                    "type": "GAME_STATE",
                    "state": state
                })

    except WebSocketDisconnect:
        manager.disconnect(player_id)

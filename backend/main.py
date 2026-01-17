from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from room_manager import (
    create_room,
    join_room,
    get_room,
    remove_player
)
from game_logic import (
    start_game,
    play_card,
    draw_card
)

app = FastAPI()

# websocket -> player_id
connections = {}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    player_id = f"p_{id(ws)}"
    connections[ws] = player_id

    try:
        while True:
            message = await ws.receive_json()
            msg_type = message.get("type")

            # 1️⃣ CREATE ROOM
            if msg_type == "create_room":
                room = create_room(player_id)
                await ws.send_json({
                    "type": "room_created",
                    "room": room
                })

            # 2️⃣ JOIN ROOM
            elif msg_type == "join_room":
                room_code = message.get("room_code")
                room = join_room(room_code, player_id)

                if not room:
                    await ws.send_json({
                        "type": "error",
                        "message": "Room not found"
                    })
                    continue

                # notify all players in room
                for conn, pid in connections.items():
                    if pid in room["players"]:
                        await conn.send_json({
                            "type": "lobby_update",
                            "room": room
                        })

            # 3️⃣ START GAME (host only)
            elif msg_type == "start_game":
                room_code = message.get("room_code")
                game_state = start_game(room_code)

                room = get_room(room_code)
                for conn, pid in connections.items():
                    if pid in room["players"]:
                        await conn.send_json({
                            "type": "game_started",
                            "game": game_state
                        })

            # 4️⃣ PLAY CARD
            elif msg_type == "play_card":
                result = play_card(
                    room_code=message["room_code"],
                    player_id=player_id,
                    card_id=message["card_id"]
                )

                room = get_room(message["room_code"])
                for conn, pid in connections.items():
                    if pid in room["players"]:
                        await conn.send_json({
                            "type": "game_update",
                            "game": result
                        })

            # 5️⃣ DRAW CARD
            elif msg_type == "draw_card":
                result = draw_card(
                    room_code=message["room_code"],
                    player_id=player_id
                )

                room = get_room(message["room_code"])
                for conn, pid in connections.items():
                    if pid in room["players"]:
                        await conn.send_json({
                            "type": "game_update",
                            "game": result
                        })

    except WebSocketDisconnect:
        remove_player(player_id)
        del connections[ws]
        print(f"{player_id} disconnected")

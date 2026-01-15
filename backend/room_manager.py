rooms = {}

def create_room(room_code, player_id):
    rooms[room_code] = {
        "code": room_code,
        "host": player_id,
        "players": [player_id]
    }
    return rooms[room_code]

def join_room(room_code, player_id):
    room = rooms.get(room_code)
    if not room:
        return None

    if player_id not in room["players"]:
        room["players"].append(player_id)

    return room

def can_start_game(room, player_id):
    return player_id == room["host"] and len(room["players"]) >= 2

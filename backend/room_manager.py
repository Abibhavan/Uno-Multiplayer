import random
import string
from game_logic import start_game

# room_code -> room_data
rooms = {}

def _generate_room_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_room(host_player_id):
    """
    Creates a new room and assigns the host.
    """
    code = _generate_room_code()

    rooms[code] = {
        "code": code,
        "host": host_player_id,
        "players": [host_player_id],
        "game_started": False
    }

    return serialize_room(rooms[code])

def join_room(code, player_id):
    """
    Adds a player to an existing room.
    """
    room = rooms.get(code)
    if not room:
        return None

    if room["game_started"]:
        return None  # prevent joining mid-game

    if player_id not in room["players"]:
        room["players"].append(player_id)

    return serialize_room(room)

def start_room_game(code):
    """
    Starts the game for a room (host only).
    """
    room = rooms.get(code)
    if not room:
        return None

    room["game_started"] = True

    game_state = start_game(
        room_code=code,
        players=room["players"]
    )

    return game_state

def remove_player(player_id):
    """
    Removes a player from their room on disconnect.
    """
    for code, room in list(rooms.items()):
        if player_id in room["players"]:
            room["players"].remove(player_id)

            # If host leaves, destroy room
            if player_id == room["host"]:
                del rooms[code]
                return

            # If room empty, destroy it
            if not room["players"]:
                del rooms[code]
                return

def get_room(code):
    return rooms.get(code)

def serialize_room(room):
    """
    Removes internal-only fields before sending to frontend.
    """
    return {
        "code": room["code"],
        "host": room["host"],
        "players": room["players"]
    }

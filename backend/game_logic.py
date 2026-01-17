from deck import create_deck, draw_cards
import random

games = {}  # room_code -> game_state


def start_game(room_code, players):
    """
    Initializes a new UNO game for a room.
    """
    deck = create_deck()
    random.shuffle(deck)

    hands = {player: [] for player in players}

    # Deal 7 cards to each player
    for _ in range(7):
        for player in players:
            hands[player].append(deck.pop())

    # Pick first non-wild card
    while True:
        first_card = deck.pop()
        if first_card["color"] != "wild":
            break
        deck.insert(0, first_card)

    game_state = {
        "room_code": room_code,
        "players": players,
        "hands": hands,
        "deck": deck,
        "discard_pile": [first_card],
        "current_player": players[0],
        "direction": 1,  # 1 = clockwise, -1 = counter
        "current_color": first_card["color"],
        "winner": None
    }

    games[room_code] = game_state
    return serialize_game_state(game_state)


# -------------------------
# CORE GAME ACTIONS
# -------------------------

def play_card(room_code, player_id, card, chosen_color=None):
    game = games.get(room_code)
    if not game:
        return {"error": "Game not found"}

    if game["winner"]:
        return {"error": "Game already finished"}

    if player_id != game["current_player"]:
        return {"error": "Not your turn"}

    if card not in game["hands"][player_id]:
        return {"error": "Card not in hand"}

    top_card = game["discard_pile"][-1]

    if not is_valid_move(card, top_card, game["current_color"]):
        return {"error": "Invalid move"}

    game["hands"][player_id].remove(card)
    game["discard_pile"].append(card)

    apply_card_effect(game, card, chosen_color)
    check_winner(game, player_id)

    if not game["winner"]:
        advance_turn(game)

    return serialize_game_state(game)


def draw_card(room_code, player_id):
    game = games.get(room_code)
    if not game or player_id != game["current_player"]:
        return {"error": "Invalid draw"}

    card = game["deck"].pop()
    game["hands"][player_id].append(card)

    advance_turn(game)
    return serialize_game_state(game)


# -------------------------
# VALIDATION & RULES
# -------------------------

def is_valid_move(card, top_card, current_color):
    if card["color"] == "wild":
        return True

    return (
        card["color"] == current_color or
        card["value"] == top_card["value"]
    )


def apply_card_effect(game, card, chosen_color):
    value = card["value"]

    if card["color"] == "wild":
        game["current_color"] = chosen_color

        if value == "wild_draw_4":
            next_player = get_next_player(game)
            draw_cards(game, next_player, 4)
            skip_turn(game)

    elif value == "skip":
        skip_turn(game)

    elif value == "reverse":
        game["direction"] *= -1

        # Special case: 2 players → acts like skip
        if len(game["players"]) == 2:
            skip_turn(game)

    elif value == "draw_2":
        next_player = get_next_player(game)
        draw_cards(game, next_player, 2)
        skip_turn(game)

    else:
        game["current_color"] = card["color"]


# -------------------------
# TURN HANDLING
# -------------------------

def advance_turn(game):
    idx = game["players"].index(game["current_player"])
    next_idx = (idx + game["direction"]) % len(game["players"])
    game["current_player"] = game["players"][next_idx]


def skip_turn(game):
    advance_turn(game)


def get_next_player(game):
    idx = game["players"].index(game["current_player"])
    next_idx = (idx + game["direction"]) % len(game["players"])
    return game["players"][next_idx]


# -------------------------
# WIN CHECK
# -------------------------

def check_winner(game, player_id):
    if not game["hands"][player_id]:
        game["winner"] = player_id


# -------------------------
# SERIALIZATION
# -------------------------

def serialize_game_state(game):
    """
    Removes private information before sending to frontend.
    """
    return {
        "room_code": game["room_code"],
        "players": game["players"],
        "hands_count": {
            p: len(game["hands"][p]) for p in game["players"]
        },
        "your_hand": game["hands"],
        "top_card": game["discard_pile"][-1],
        "current_player": game["current_player"],
        "current_color": game["current_color"],
        "direction": game["direction"],
        "winner": game["winner"]
    }

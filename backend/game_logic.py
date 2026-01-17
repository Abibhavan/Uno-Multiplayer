import random
from deck import create_deck, draw_cards

games = {}


def start_game(room_code, players):
    deck = create_deck()
    hands = {p: [] for p in players}

    for _ in range(7):
        for p in players:
            hands[p].append(deck.pop())

    while True:
        first = deck.pop()
        if first["color"] != "wild":
            break
        deck.insert(0, first)

    game = {
        "room": room_code,
        "players": players,
        "hands": hands,
        "deck": deck,
        "discard_pile": [first],
        "current_player": players[0],
        "direction": 1,
        "current_color": first["color"],
        "winner": None
    }

    games[room_code] = game
    return serialize(game)


def play_card(room, player, card, chosen_color=None):
    game = games.get(room)
    if not game:
        return error("Game not found")

    if game["winner"]:
        return error("Game finished")

    if player != game["current_player"]:
        return error("Not your turn")

    if card not in game["hands"][player]:
        return error("Card not in hand")

    top = game["discard_pile"][-1]

    if not valid(card, top, game["current_color"]):
        return error("Invalid move")

    game["hands"][player].remove(card)
    game["discard_pile"].append(card)

    apply_effect(game, card, chosen_color)

    if not game["hands"][player]:
        game["winner"] = player
    else:
        advance_turn(game)

    return serialize(game)


def draw_card(room, player):
    game = games.get(room)
    if player != game["current_player"]:
        return error("Not your turn")

    draw_cards(game, player, 1)
    advance_turn(game)
    return serialize(game)


# ---------- RULES ----------

def valid(card, top, current_color):
    if card["color"] == "wild":
        return True
    return card["color"] == current_color or card["value"] == top["value"]


def apply_effect(game, card, chosen_color):
    val = card["value"]

    if card["color"] == "wild":
        game["current_color"] = chosen_color
        if val == "wild_draw_5":
            victim = next_player(game)
            draw_cards(game, victim, 5)
            skip(game)
        return

    game["current_color"] = card["color"]

    if val == "skip":
        skip(game)
    elif val == "reverse":
        game["direction"] *= -1
        if len(game["players"]) == 2:
            skip(game)
    elif val == "draw_2":
        victim = next_player(game)
        draw_cards(game, victim, 2)
        skip(game)


# ---------- TURN HANDLING ----------

def advance_turn(game):
    idx = game["players"].index(game["current_player"])
    game["current_player"] = game["players"][(idx + game["direction"]) % len(game["players"])]


def skip(game):
    advance_turn(game)


def next_player(game):
    idx = game["players"].index(game["current_player"])
    return game["players"][(idx + game["direction"]) % len(game["players"])]


# ---------- SERIALIZATION ----------

def serialize(game):
    return {
        "room": game["room"],
        "players": game["players"],
        "hands_count": {p: len(game["hands"][p]) for p in game["players"]},
        "top_card": game["discard_pile"][-1],
        "current_player": game["current_player"],
        "current_color": game["current_color"],
        "direction": game["direction"],
        "winner": game["winner"]
    }


def error(msg):
    return {"error": msg}

import random

COLORS = ["red", "yellow", "green", "blue"]
VALUES = [str(i) for i in range(10)] + ["skip", "reverse", "draw_2"]
WILD_VALUES = ["wild", "wild_draw_4"]


def create_deck():
    deck = []

    for color in COLORS:
        deck.append({"color": color, "value": "0"})

        for value in VALUES[1:]:
            deck.append({"color": color, "value": value})
            deck.append({"color": color, "value": value})

    for _ in range(4):
        for value in WILD_VALUES:
            deck.append({"color": "wild", "value": value})

    random.shuffle(deck)
    return deck


def draw_cards(game, player_id, count):
    for _ in range(count):
        if not game["deck"]:
            reshuffle(game)
        game["hands"][player_id].append(game["deck"].pop())


def reshuffle(game):
    top = game["discard_pile"][-1]
    game["deck"] = game["discard_pile"][:-1]
    game["discard_pile"] = [top]
    random.shuffle(game["deck"])

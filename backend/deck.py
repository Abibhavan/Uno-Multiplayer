import uuid
import random

COLORS = ["red", "green", "blue", "yellow"]
NUMBER_VALUES = list(range(10))
ACTION_TYPES = ["skip", "reverse", "draw_two"]

def generate_card(color, card_type, value=None):
    return {
        "id": f"c_{uuid.uuid4().hex[:8]}",
        "color": color,
        "type": card_type,
        "value": value
    }

def generate_uno_deck():
    deck = []

    # Colored cards
    for color in COLORS:
        # One zero
        deck.append(generate_card(color, "number", 0))

        # Two of each 1–9
        for num in range(1, 10):
            deck.append(generate_card(color, "number", num))
            deck.append(generate_card(color, "number", num))

        # Action cards (2 each)
        for action in ACTION_TYPES:
            deck.append(generate_card(color, action))
            deck.append(generate_card(color, action))

    # Wild cards (no color)
    for _ in range(4):
        deck.append(generate_card(None, "wild"))
        deck.append(generate_card(None, "wild_draw_four"))

    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

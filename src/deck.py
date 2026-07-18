from .card import Card
import random

class Deck:
    def __init__(self, empty = False):
        self.cards = []

        if not empty:
            self._build()
            self.shuffle()

    def _build(self):
        suits = ["♡", "♢", "♣", "♠"]
        values = range(1, 14)

        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
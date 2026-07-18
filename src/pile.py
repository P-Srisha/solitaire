class Pile:
    def __init__(self, pile_type):
        self.cards = []
        self.pile_type = pile_type # tableau, stock, waste, foundation

    def add(self, card):
        self.cards.append(card)

    def remove(self):
        if len(self.cards) == 0: 
            return None
        return self.cards.pop()

    def top(self):
        if len(self.cards) == 0:
            return None
        return self.cards[-1]
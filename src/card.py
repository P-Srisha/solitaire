class Card:
    def __init__(self, suit, value, face_up = False):
        self.suit = suit
        self.value = value
        self.face_up = face_up

    def color(self):
        if self.suit in ["♡", "♢"]:
            return "red"
        else:
            return "black"
        
    def __str__(self):
        if not self.face_up:
            return "▓▓"
        
        value_map = {1: "A", 11: "J", 12: "Q", 13: "K"}

        display_value = value_map.get(self.value, str(self.value));
        return f"{display_value}{self.suit}"
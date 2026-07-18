class GamePrinter:
    def __init__(self, game):
        self.game = game
        
    def print_board(self):
        game = self.game

        print("\n-----SOLITAIRE-----\n")

        print("Foundations: ")
        for i, f in enumerate(game.foundations): #go through each foundation pile
            top = f.top()
            if top:
                print(f"  F{i}: {top}")
            else:
                print(f"  F{i}: [empty]")

        print("\nStock / Waste: ")
        print(f"  Stock: {len(game.stock.cards)} cards")
        if game.waste.top(): # i.e waste is not empty
            print(f"  Waste: {game.waste.top()}")
        else:
            print(f"  Waste: [empty]")

        print("\nTableau: ")
        for i, pile in enumerate(game.tableau):
            line = []
            for card in pile.cards:
                line.append(str(card))
            print(f"  T{i}: {' '.join(line)}")

            
        status = f"Moves: {self.game.move_count} | Undo: {len(self.game.history)} | Stock: {len(self.game.stock.cards)}"

        if self.game.can_auto_finish():
            status += " | Auto-finish available"

        print("\n" + status)
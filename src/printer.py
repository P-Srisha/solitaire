class GamePrinter:
    def __init__(self, game):
        self.game = game
        
    def print_board(self):
        game = self.game

        print("\n════════════════════════════════════")
        print("      ♠ KLONDIKE SOLITAIRE ♡")
        print("════════════════════════════════════\n")

        print("Foundations: ")
        for i, foundation in enumerate(game.foundations):
            top = foundation.top()
            
            if top:
                print(f"  {top.suit}  {top}")
            else:
                print("  □  —")

        print("\nStock / Waste: ")
        print(f"  🂠 Stock: {len(game.stock.cards)} cards")
        print(f"  🂡 Waste : {game.waste.top() if game.waste.top() else '—'}")
        # if game.waste.top(): # i.e waste is not empty
        #     print(f"  Waste: {game.waste.top()}")
        # else:
        #     print(f"  Waste: [empty]")

        print("\nTableau: ")
        for i, pile in enumerate(game.tableau):
            line = []
            for card in pile.cards:
                line.append(str(card))
            print(f"  T{i:<2}| {' '.join(line)}")

            
        print("\n────────────────────────────────────")
        status = f"Moves: {self.game.move_count} | Undo: {len(self.game.history)} | Stock: {len(self.game.stock.cards)}"

        if self.game.can_auto_finish():
            status += " | Auto-finish available"

        print(status)
        print("────────────────────────────────────")
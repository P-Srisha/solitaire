from .deck import Deck
from .pile import Pile
from .move import Move


class Game:
    def __init__(self):
        self.history = []
        self.setup()
        self.move_count = 0

    # ====== SETUP ======
    def setup(self):
        self.deck = Deck()

        self.initial_deck_state = list(self.deck.cards)

        self.tableau = [Pile("tableau") for _ in range(7)]
        self.stock = Pile("stock")
        self.waste = Pile("waste")
        foundation_suits = ["♡", "♢", "♣", "♠"]
        self.foundations = [Pile("foundation", suit) for suit in foundation_suits]

        for i in range(7):
            for j in range(i+1):
                card = self.deck.draw()
                self.tableau[i].add(card)
            
            top_card = self.tableau[i].top()
            top_card.face_up = True

        while True:
            card = self.deck.draw()
            if card is None:
                break
            self.stock.add(card)
   
    
    # ====== NEW GAME ======
    def new_game(self):
        self.history.clear()
        self.move_count = 0
        self.setup()

    # ====== RESET BOARD ======
    def reset_board(self):
        self.history.clear()
        self.move_count = 0

        self.deck.cards = list(self.initial_deck_state)

        self.tableau = [Pile("tableau") for _ in range(7)]
        self.stock = Pile("stock")
        self.waste = Pile("waste")
        self.foundations = [Pile("foundation") for _ in range(4)]

        for i in range(7):
            for j in range(i+1):
                card = self.deck.draw()
                card.face_up = False
                self.tableau[i].add(card)
            
            top_card = self.tableau[i].top()
            top_card.face_up = True
        
        while self.deck.cards:
            card = self.deck.draw()
            card.face_up = False
            self.stock.add(card)
            
    # ====== DEBUGGING HELPERS ======
    def count_all_cards(self):
        total = 0

        for pile in self.tableau:
            total += len(pile.cards)

        total += len(self.stock.cards)
        total += len(self.waste.cards)

        for pile in self.foundations:
            total += len(pile.cards)

        print(f"Total cards: {total}")

    def check_tableau_sizes(self):
        for i, pile in enumerate(self.tableau):
            print(f"Tableau {i}: {len(pile.cards)} cards")

    def check_face_up(self):
        for i, pile in enumerate(self.tableau):
            for j, card in enumerate(pile.cards):
                if j == len(pile.cards) - 1:
                    print(f"Tableau {i} top card face_up =", card.face_up)
                else:
                    print(f"Tableau {i} card {j} face_up =", card.face_up) 

    def check_stock_size(self):
        print(f"Stock size: {len(self.stock.cards)}")      

    def debug_checks(self):
        self.count_all_cards()
        self.check_tableau_sizes()
        self.check_face_up()     
        self.check_stock_size()


    # ====== GAME LOGIC ======
    def draw_from_stock(self):
        # save state before making changes
        # if self.stock.cards or self.waste.cards:
        #     self.save_state()

        # when stock is not empty
        if len(self.stock.cards) > 0: # if self.stock.cards:
            card = self.stock.remove()
            card.face_up = True
            self.waste.add(card)

            self.history.append({
                "type": "draw",
                "card": card
            })
            self.move_count += 1
            return # so that fn returns if this stock is not empty
        
        # when stock is empty
        # as long as waste is not empty you remove from waste face down and then add to stock
        if self.waste.cards: # if self.waste.cards
            moved_cards = []

            while self.waste.cards:
                card = self.waste.remove()
                card.face_up = False
                self.stock.add(card)
                moved_cards.append(card)

            self.history.append({
                "type": "recycle",
                "cards": moved_cards
            })

            self.move_count += 1
        

    def is_valid_move(self, move):
        # checking if source or dest piles exist
        if move.source is None or move.dest is None:
            return False
        # checking if source is empty
        if len(move.source.cards) < 1: # if not move.source.cards:
            return False
        # checking if either cards to be moved is atleast 1 in number 
        # OR checking if cards to be moved are moved than present in the source pile
        if move.count < 1 or move.count > len(move.source.cards):
            return False
        # checking if all the cards to be moved are face up
        cards_to_move = move.source.cards[-move.count:]
        

        if not all(card.face_up for card in cards_to_move):
            return False
            
        # okay so first check if its Tableau to Tableau
        # then first rule says compare the bottom of the moving pile and the top of dest pile
        # they must be of oppsoite colors and the top of dest must be exactly one more than the bottom of moving pile
        # so cards_to_move : 0-> bottom and -1-> top ov moving stack
        # TABLEAU TO TABLEAU
        if move.source.pile_type == "tableau" and move.dest.pile_type == "tableau":
            moving_card = cards_to_move[0]
            dest_top = move.dest.top()

            if dest_top is None: # means that dest tableau is empty
                if moving_card.value != 13:
                    return False
                
            else:
                if moving_card.color() == dest_top.color():
                    return False
                if moving_card.value != dest_top.value - 1:
                    return False
                

        # WASTE TO TABLEAU
        if move.source.pile_type == "waste" and move.dest.pile_type == "tableau":
            if move.count != 1:
                return False
            
            waste_card = move.source.top()
            dest_top = move.dest.top()

            if dest_top is None: #means dest tableau is empty
                if waste_card.value != 13:
                    return False
            else:
                if dest_top.color() == waste_card.color():
                    return False
                if waste_card.value != dest_top.value - 1:
                    return False
                
        # FOUNDATION RULES
        # TABLEAU TO FOUNDATION
        if move.dest.pile_type == "foundation" and move.source.pile_type in ("tableau", "waste"):
            if move.count != 1: 
                return False
            dest_top = move.dest.top()
            moving_card = move.source.top()

            if dest_top is None: # meaning dest i.e foundation is empty
                if moving_card.value != 1:
                    return False
            else:
                if moving_card.suit != dest_top.suit:
                    return False
                if moving_card.value != dest_top.value + 1:
                    return False

        return True
    
    def execute_move(self, move):
        if not self.is_valid_move(move):
            return False
        
        cards_to_move = move.source.cards[-move.count:]
        flipped_card = None

        for _ in range(move.count):
            move.source.remove()

        for card in cards_to_move:
            move.dest.add(card)

        if move.source.pile_type == "tableau":
            top_card = move.source.top()
            if top_card is not None and not top_card.face_up:
                top_card.face_up = True
                flipped_card = top_card

        self.history.append({
            "source" : move.source,
            "dest" : move.dest,
            "cards" : cards_to_move,
            "flipped" : flipped_card
        })

        self.move_count += 1

        return True
    
    # def is_won(self):
    #     for foundation in self.foundations:
    #         if len(foundation.cards) != 13:
    #             return False
    #     return True

    def is_won(self):
        return all(len(foundation.cards) == 13 for foundation in self.foundations)
    
    # ====== EFFECTIVELY WON =======
    def is_effectively_won(self):
        return all(card.face_up for pile in self.tableau for card in pile.cards)
    #after this check for auto finish condition which is written below under the polishing section

    # ====== POLISHING ======
    # this function is to just check if the auto move to founation is a valid move
    def find_safe_foundation_move(self):
        # tableau to foundation
        # check if tableau top card is Ace or 2 only
        for pile in self.tableau:
            if not pile.cards: # if tableau is empty
                continue

            card = pile.top()

            # only face up cards can move from tableau
            if not card.face_up:
                continue
            
            for foundation in self.foundations:
                move = Move(pile, foundation, 1) #try moving this tableau card to all foundations and see what works
                if self.is_valid_move(move):
                    return move
            
        # waste to foundation
        if self.waste.cards: # if its not empty 
            for foundation in self.foundations:
                move = Move(self.waste, foundation, 1)
                if self.is_valid_move(move):
                    return move
            
        return None # if its not valid 
    
    # this function is for auto moving to foundation
    def auto_move_to_foundation(self):
        moved_any = False

        while True:
            move = self.find_safe_foundation_move()
            if not move: # meaning there is no valid move
                break

            self.execute_move(move)
            moved_any = True
        
        return moved_any
    

    # ===== UNDO ======
    def undo(self):
        if not self.history: # there is no history
            print("Nothing to undo.")
            return False

        previous = self.history.pop()
        
        #======= MOVE UNDO =======
        if "source" in previous:
            source = previous["source"]
            dest = previous["dest"]
            cards = previous["cards"]
            flipped = previous["flipped"]

            for _ in range(len(cards)):
                dest.remove()

            for card in cards:
                source.add(card)

            if flipped:
                flipped.face_up = False

            self.move_count += 1

            return True
        
        # ===== DRAW UNDO ======
        if previous["type"] == "draw":
            card = previous["card"]

            self.waste.remove()
            card.face_up = False
            self.stock.add(card)

            self.move_count += 1

            return True
        
        # ====== RECYCLE UNDO =======
        if previous["type"] == "recycle":
            cards = previous["cards"]

            for _ in range(len(cards)):
                card = self.stock.remove()
                card.face_up = True
                self.waste.add(card)

            self.move_count += 1

            return True
        
        return False

            

    # ====== AUTO FINISH ======
    def can_auto_finish(self):
        return self.is_effectively_won()
    
    def auto_finish(self):
        while True:
            moved = self.auto_move_to_foundation()
            if not moved:
                break
    
    # ====== HELPER =======
    def help_function(self):
        commands = [
            ("m <src> <dest> <count>", "move cards"),
            ("d", "draw from stock"),
            ("u", "undo move"),
            ("a", "auto-move to foundation"),
            ("r", "reset board"),
            ("n", "new game"),
            ("q", "quit"),
            ("h", "help")
        ]
        print("\nCommands:\n")
        for cmd, desc in commands:
            print(f"{cmd:<25} {desc}")
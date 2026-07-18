from .printer import GamePrinter
from .game import Game
from .move import Move


game = Game()
printer = GamePrinter(game)
printer.print_board()

while True:
    cmd = input("Command (d=draw, m=move, a=auto-move, u=undo, r=restart,n=new-game, h=help, q=quit): ").strip().lower()

    if game.can_auto_finish() and not game.is_won():
        print("Auto finish available. Press [f] to finish.")

    if cmd == "q":
        print("Exiting. Thanks for playing! \n")
        break

    elif cmd == "d":
        game.draw_from_stock()
        printer.print_board()

    elif cmd == "a":
        if game.auto_move_to_foundation():
            print("Auto-moved safe cards to foundation.")
        else:
            print("No safe auto-moves available.")
        printer.print_board()
        
    elif cmd == "u":
        game.undo()
        printer.print_board()

    elif cmd == "r":
        game.reset_board()
        printer.print_board()

    elif cmd == "n":
        game.new_game()
        printer.print_board()
    
    elif cmd == "h":
        game.help_function()
        printer.print_board()
        
    elif cmd == "f":
        if game.can_auto_finish():
            game.auto_finish()
            printer.print_board()
        else:
            print("Auto-finish not available.")
    
    elif cmd.startswith("m"):
        try:
            parts = cmd.split()

            if len(parts) != 4:
                print("Usage: m <source> <dest> <count>")
                continue

            _, src, dst, count_str = parts
            count = int(count_str)
        
            def get_pile(code):
                if code.startswith("t"):
                    return game.tableau[int(code[1])]
                if code.startswith("f"):
                    return game.foundations[int(code[1])]
                if code == "w":
                    return game.waste
                return None

            source = get_pile(src)
            dest = get_pile(dst)

            move = Move(source, dest, count)

            if game.execute_move(move):
                print("Move OK")
            else:
                print("Invalid move")

            printer.print_board()
            
        except Exception as e:
            print("Error:", e)
        
    if game.is_won():
        print("\n" + "="*40)
        print("CONGRATS, YOU WON!!!")
        print(f"Moves: {game.move_count}")
        print("[r] Reset board | [n] New Game | [q] Quit")
        print("="*40)
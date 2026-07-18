# Klondike Solitaire Engine

A command-line implementation of **Klondike Solitaire** written in Python. The project recreates the classic card game while emphasizing clean object-oriented design, modular architecture, and rule-based game logic.

---

## Features

- Standard 52-card deck with randomized shuffling
- Complete Klondike Solitaire gameplay
- Rule-based move validation
- Undo functionality
- Automatic moves to foundation
- Win condition detection
- Modular Object-Oriented design

---

## Screenshot

![Gameplay](screenshots\Solitaire_gameplay.png)

---

## Project Structure

```text
solitaire/
├── src/
|  ├── card.py
|  ├── deck.py
|  ├── pile.py
|  ├── move.py
|  ├── game.py
|  ├── printer.py
|  ├── main.py
├── screenshots
|  ├── Solitaire_gameplay.png
├── README.md
└── .gitignore
```

---

## Class Design

| Class | Responsibilty |
|:-----:|:-------------:|
| `Card` | Represents an individual playing card |
| `Deck` | Creates and shuffles the deck |
| `Pile` | Implements tableau, stock, waste and foundation piles |
| `Move` | Stores move information for execution and undo |
| `Game` | Manages game state and enforces Solitaire rules |
| `GamePrinter` | Renders the game board in the terminal |

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/P-Srisha/solitaire.git
cd solitaire
```

Run the game:

```bash
python -m src.main
```

---

## Gameplay

Players can:

- Draw cards from the stock
- Move cards between tableau piles
- Move cards to foundation piles
- Undo previous moves
- Automatically move eligible cards to foundation
- Automatically finish the game when possible

---

## Technologies

- Python
- Object-Oriented Programming (OOP)
- Command-Line Interface (CLI)

---

## Future Improvements

- Colored terminal interface
- Save and load game state
- Hint system
- Multiple Solitaire variants
- GUI Version

# 21 Number Game

A terminal-based Python implementation of the classic **21 Number Game** (also known as Twenty-One or Bagram), played against the computer.

## Description

Two players — you and the computer — take turns counting from 1 to 21. On each turn, a player must call out **1 to 3 consecutive numbers**. The numbers continue from where the last player left off. The player who is forced to say **21 loses**.

The computer uses a mathematical strategy based on multiples of 4 to maximize its chances of winning.

## Rules

1. The game always starts at **1**.
2. On each turn, a player says **1, 2, or 3** consecutive numbers.
3. Numbers must be consecutive with no gaps.
4. The first number you say must be the next number in sequence.
5. **Whoever says 21 loses.**
6. You can choose to go **first** or **second**.

## Computer Strategy

The computer targets specific numbers: **4, 8, 12, 16, and 20**.

By always ending its turn on one of these positions, the computer forces the player into a position where they must eventually say 21. The key insight is:

- If the computer says 20, the next number is 21 — and the player must say it.
- By reaching each multiple of 4 in sequence, the computer maintains control throughout the game.

If the computer cannot reach the next target in a single turn (because it would require more than 3 numbers), it advances just one step and re-adjusts on the next turn.

## Features

- Choose to go first or second
- Input validation with clear error messages
- Consecutive number checking
- Computer opponent with optimal strategy
- Play again option after each round
- Case-insensitive input handling

## Requirements

- Python 3.8 or higher
- No external dependencies to play; pytest is required for tests

## Installation

Clone the repository:

```bash
git clone https://github.com/kshres31/21_number_game.git
cd 21_number_game
```

No additional packages need to be installed.

## Running the Game

```bash
python main.py
```

## Testing

Install pytest, then run the automated tests from the project directory:

```bash
python -m pip install pytest
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

## Example Gameplay

```
================================
        21 NUMBER GAME
================================

You and the computer take turns calling
1 to 3 consecutive numbers.

Whoever says 21 loses.

Do you want to go first or second? > first

--- Your turn (current: 1) ---
How many numbers? (1-3) > 3
Enter 3 number(s) starting from 1: > 1 2 3
You said: 1 2 3
Current number is now 4.

--- Computer's turn (current: 4) ---
Computer says: 4
Current number is now 5.

--- Your turn (current: 5) ---
How many numbers? (1-3) > 1
Enter 1 number(s) starting from 5: > 5
You said: 5
Current number is now 6.

--- Computer's turn (current: 6) ---
Computer says: 6 7 8
Current number is now 9.
...
```

## Project Structure

```
├── main.py          # Game loop and user interface
├── game.py          # Core game logic and computer strategy
├── test_game.py     # Automated tests
├── README.md        # This file
└── .gitignore       # Python-specific ignores
```

## License

This project is for educational purposes.

"""21 Number Game — Player vs Computer.

The game counts from 1 to 21. Each turn a player calls 1-3 consecutive
numbers. Whoever is forced to say 21 loses.
"""

from game import MAX_NUMBER, TURN_LIMIT, validate_move, computer_move, move_includes_losing_number


def show_banner():
    print("=" * 36)
    print("        21 NUMBER GAME")
    print("=" * 36)
    print()
    print("You and the computer take turns calling")
    print("1 to 3 consecutive numbers.")
    print()
    print("Whoever says 21 loses.")
    print()


def ask_first_or_second():
    """Ask the player whether they want to go first or second."""
    while True:
        choice = input("Do you want to go first or second? > ").strip().lower()
        if choice in ("first", "f"):
            return True  # player goes first
        if choice in ("second", "s"):
            return False  # player goes second
        print("Please enter 'first' or 'second'.")


def ask_number_count():
    """Ask the player how many numbers they want to say (1-3)."""
    while True:
        raw = input(f"How many numbers? (1-{TURN_LIMIT}) > ").strip()
        try:
            count = int(raw)
        except ValueError:
            print("Please enter a number.")
            continue
        if count < 1 or count > TURN_LIMIT:
            print(f"You must choose between 1 and {TURN_LIMIT}.")
            continue
        return count


def ask_numbers(count, current):
    """Ask the player to enter *count* numbers starting from *current*.

    Accepts space-separated input on a single line.
    Returns a list of integers or None if input was invalid.
    """
    while True:
        raw = input(f"Enter {count} number(s) starting from {current}: > ").strip()
        parts = raw.split()
        if len(parts) != count:
            print(f"Expected {count} number(s), got {len(parts)}. Try again.")
            continue
        try:
            numbers = [int(p) for p in parts]
        except ValueError:
            print("Please enter valid whole numbers separated by spaces.")
            continue
        return numbers


def play_round():
    """Run a single round of the 21 Number Game.

    Returns the winner: "player" or "computer".
    """
    player_first = ask_first_or_second()
    print()

    current = 1
    player_turn = player_first

    while current <= MAX_NUMBER:
        if player_turn:
            print(f"\n--- Your turn (current: {current}) ---")
            count = ask_number_count()
            numbers = ask_numbers(count, current)

            ok, msg = validate_move(numbers, current)
            if not ok:
                print(f"Invalid move: {msg}")
                print("You lose this round!")
                return "computer"

            print(f"You said: {' '.join(map(str, numbers))}")
            current = numbers[-1] + 1

            if move_includes_losing_number(numbers):
                print("\nYou said 21 — YOU LOSE!")
                return "computer"

            # Show game state
            if current <= MAX_NUMBER:
                print(f"Current number is now {current}.")
        else:
            print(f"\n--- Computer's turn (current: {current}) ---")
            numbers = computer_move(current)
            print(f"Computer says: {' '.join(map(str, numbers))}")
            current = numbers[-1] + 1

            if move_includes_losing_number(numbers):
                print("\nThe computer said 21 — YOU WIN!")
                return "player"

            if current <= MAX_NUMBER:
                print(f"Current number is now {current}.")

        player_turn = not player_turn

    # Fallback — should not normally be reached
    return "draw"


def main():
    show_banner()

    while True:
        winner = play_round()
        if winner == "player":
            print("\nCongratulations — you won!")
        else:
            print("\nBetter luck next time!")

        print()
        while True:
            again = input("Would you like to play again? (y/n): > ").strip().lower()
            if again in ("y", "yes"):
                break
            if again in ("n", "no"):
                print("\nThanks for playing!")
                return
            print("Please enter 'y' or 'n'.")
        print()


if __name__ == "__main__":
    main()

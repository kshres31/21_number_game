"""Core logic for the 21 Number Game."""

MAX_NUMBER = 21
TURN_LIMIT = 3
# The computer targets these numbers. Landing on one means the opponent
# is forced closer to 21, and the player who says 21 loses.
TARGETS = {4, 8, 12, 16, 20}


def validate_move(numbers, current):
    """Check whether a list of integers is a legal move from *current*.

    Returns (ok, message) where *ok* is True for a valid move and *message*
    explains any problem.
    """
    if not numbers:
        return False, "You must say at least one number."

    if len(numbers) > TURN_LIMIT:
        return False, f"You can say at most {TURN_LIMIT} numbers at a time."

    for n in numbers:
        if not isinstance(n, int):
            return False, "All numbers must be whole numbers."
        if n < 1 or n > MAX_NUMBER:
            return False, f"Numbers must be between 1 and {MAX_NUMBER}."

    if numbers[0] != current:
        return False, f"First number must be {current} (the next in sequence)."

    # Verify consecutiveness
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1] + 1:
            return False, "Numbers must be consecutive with no gaps."

    return True, "OK"


def computer_move(current):
    """Pick the computer's numbers using the multiples-of-4 strategy.

    The computer tries to be the one who says 4, 8, 12, 16, or 20 so that
    the opponent is eventually forced to say 21.
    """
    # Smallest multiple of 4 that is >= current
    target = ((current + 3) // 4) * 4
    count = target - current + 1

    if 1 <= count <= TURN_LIMIT:
        return list(range(current, target + 1))

    # Can't reach the target in one move — just advance one step.
    return [current]


def move_includes_losing_number(numbers):
    """Return True if the move includes 21 (the losing number)."""
    return MAX_NUMBER in numbers

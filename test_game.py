"""Tests for the 21 Number Game logic."""

import pytest
from game import (
    MAX_NUMBER,
    TURN_LIMIT,
    TARGETS,
    validate_move,
    computer_move,
    move_includes_losing_number,
)


# ── Move validation ──────────────────────────────────────────────

class TestValidateMove:
    """Tests for validate_move."""

    def test_single_valid_number(self):
        ok, _ = validate_move([1], 1)
        assert ok

    def test_two_consecutive(self):
        ok, _ = validate_move([5, 6], 5)
        assert ok

    def test_three_consecutive(self):
        ok, _ = validate_move([8, 9, 10], 8)
        assert ok

    def test_empty_list_rejected(self):
        ok, msg = validate_move([], 1)
        assert not ok
        assert "at least one" in msg.lower()

    def test_four_numbers_rejected(self):
        ok, msg = validate_move([1, 2, 3, 4], 1)
        assert not ok
        assert "at most" in msg.lower()

    def test_wrong_start_rejected(self):
        ok, msg = validate_move([3, 4], 1)
        assert not ok
        assert "first number" in msg.lower()

    def test_non_consecutive_rejected(self):
        ok, msg = validate_move([5, 7], 5)
        assert not ok
        assert "consecutive" in msg.lower()

    def test_gapped_triple_rejected(self):
        ok, msg = validate_move([8, 9, 11], 8)
        assert not ok
        assert "consecutive" in msg.lower()

    def test_number_below_one_rejected(self):
        ok, msg = validate_move([0], 0)
        assert not ok
        assert "between" in msg.lower()

    def test_number_above_max_rejected(self):
        ok, msg = validate_move([22], 22)
        assert not ok
        assert "between" in msg.lower()

    def test_negative_number_rejected(self):
        ok, msg = validate_move([-1], -1)
        assert not ok

    def test_non_integer_rejected(self):
        ok, msg = validate_move([1.5], 1)
        assert not ok
        assert "whole" in msg.lower()

    def test_string_in_list_rejected(self):
        ok, msg = validate_move(["a"], 1)
        assert not ok


# ── Consecutive number checks ────────────────────────────────────

class TestConsecutiveNumbers:
    """Focused tests on consecutiveness logic."""

    @pytest.mark.parametrize("nums,start", [
        ([1, 2, 3], 1),
        ([5, 6], 5),
        ([20], 20),
        ([18, 19, 20], 18),
    ])
    def test_valid_sequences(self, nums, start):
        ok, _ = validate_move(nums, start)
        assert ok

    @pytest.mark.parametrize("nums,start", [
        ([5, 7], 5),
        ([8, 9, 11], 8),
        ([10, 12, 13], 10),
        ([1, 3], 1),
    ])
    def test_invalid_sequences(self, nums, start):
        ok, msg = validate_move(nums, start)
        assert not ok
        assert "consecutive" in msg.lower()


# ── Computer strategy ────────────────────────────────────────────

class TestComputerMove:
    """Tests for the computer's move selection."""

    def test_computer_output_is_consecutive(self):
        for start in range(1, 22):
            nums = computer_move(start)
            for i in range(1, len(nums)):
                assert nums[i] == nums[i - 1] + 1

    def test_computer_never_says_more_than_three(self):
        for start in range(1, 22):
            nums = computer_move(start)
            assert 1 <= len(nums) <= TURN_LIMIT

    def test_computer_starts_at_current(self):
        for start in range(1, 22):
            nums = computer_move(start)
            assert nums[0] == start

    def test_computer_never_goes_past_21(self):
        for start in range(1, 22):
            nums = computer_move(start)
            assert nums[-1] <= MAX_NUMBER

    def test_computer_does_not_repeat_numbers(self):
        for start in range(1, 22):
            nums = computer_move(start)
            assert len(nums) == len(set(nums))

    def test_computer_targets_multiples_of_4(self):
        """When possible, the computer should end on a multiple of 4."""
        # These start values let the computer reach the next target
        # Start=2 → target 4 (say 2,3,4)
        assert computer_move(2) == [2, 3, 4]
        # Start=3 → target 4 (say 3,4)
        assert computer_move(3) == [3, 4]
        # Start=5 → target 8 (say 5,6,7,8) but that's 4 numbers, too many
        # so computer says [5] and re-evaluates
        assert computer_move(5) == [5]
        # Start=6 → target 8 (say 6,7,8)
        assert computer_move(6) == [6, 7, 8]
        # Start=7 → target 8 (say 7,8)
        assert computer_move(7) == [7, 8]
        # Start=9 → target 12 (say 9,10,11,12) too many → [9]
        assert computer_move(9) == [9]
        # Start=10 → target 12 (say 10,11,12)
        assert computer_move(10) == [10, 11, 12]
        # Start=11 → target 12 (say 11,12)
        assert computer_move(11) == [11, 12]

    def test_computer_ends_on_target_when_possible(self):
        """Computer's last number should be a multiple of 4 when reachable."""
        for start in range(1, 21):
            nums = computer_move(start)
            target = ((start + 3) // 4) * 4
            count = target - start + 1
            if 1 <= count <= TURN_LIMIT:
                assert nums[-1] == target

    def test_computer_at_20_says_20(self):
        nums = computer_move(20)
        assert nums == [20]

    def test_computer_at_21_returns_21(self):
        nums = computer_move(21)
        assert nums == [21]


# ── Game boundaries ──────────────────────────────────────────────

class TestGameBoundaries:
    """Tests for edge cases around the losing number."""

    def test_move_includes_losing_number(self):
        assert move_includes_losing_number([19, 20, 21]) is True
        assert move_includes_losing_number([21]) is True
        assert move_includes_losing_number([20]) is False
        assert move_includes_losing_number([1, 2, 3]) is False

    def test_move_at_20_valid(self):
        ok, _ = validate_move([20], 20)
        assert ok

    def test_move_at_21_valid_but_losing(self):
        ok, _ = validate_move([21], 21)
        assert ok
        assert move_includes_losing_number([21])

    def test_cannot_skip_past_21(self):
        ok, msg = validate_move([22], 22)
        assert not ok

    def test_move_19_20_valid(self):
        ok, _ = validate_move([19, 20], 19)
        assert ok

    def test_move_19_20_21_valid_but_losing(self):
        ok, _ = validate_move([19, 20, 21], 19)
        assert ok
        assert move_includes_losing_number([19, 20, 21])


# ── Full game simulation ─────────────────────────────────────────

class TestFullGameSimulation:
    """Simulate complete games to verify the computer wins when going second."""

    def test_computer_wins_when_second(self):
        """Simulate a naive player always saying 1 number. Computer should win."""
        import random
        random.seed(42)

        current = 1
        player_turn = True  # player goes first

        while current <= MAX_NUMBER:
            if player_turn:
                # Naive player: say just 1 number
                current += 1
                if current - 1 == MAX_NUMBER:
                    return  # player said 21, computer wins
            else:
                nums = computer_move(current)
                current = nums[-1] + 1
                if move_includes_losing_number(nums):
                    pytest.fail("Computer said 21 — should not happen")

            player_turn = not player_turn

        # If we get here, the game ended. Verify player hit 21.
        assert current > MAX_NUMBER

    def test_computer_strategy_allows_no_escape(self):
        """Trace a full game where computer goes second and always targets 4."""
        current = 1
        player_turn = True
        max_turns = 100  # safety

        for _ in range(max_turns):
            if player_turn:
                # Player says 1 number
                current += 1
                if current - 1 == MAX_NUMBER:
                    return  # player loses, as expected
            else:
                nums = computer_move(current)
                current = nums[-1] + 1
                assert move_includes_losing_number(nums) is False or current - 1 == MAX_NUMBER
            player_turn = not player_turn

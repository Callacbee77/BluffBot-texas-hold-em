"""Hand ranking sanity checks. Cards are ints 0..51: rank = c % 13, suit = c // 13.
RANKS = "23456789TJQKA" so 12 = Ace, 11 = King, 0 = deuce."""

from bluffbot.evaluator import best, eval5


def card(rank, suit):
    """rank: 0..12 (2..A), suit: 0..3."""
    return suit * 13 + rank


def test_royal_flush_beats_quads():
    royal = [card(r, 0) for r in (8, 9, 10, 11, 12)]   # T-J-Q-K-A of spades
    quads = [card(12, 0), card(12, 1), card(12, 2), card(12, 3), card(5, 0)]
    assert eval5(royal) > eval5(quads)


def test_wheel_is_a_five_high_straight():
    wheel = [card(12, 0), card(0, 1), card(1, 2), card(2, 3), card(3, 0)]
    six_high = [card(0, 0), card(1, 1), card(2, 2), card(3, 3), card(4, 0)]
    assert eval5(wheel)[0] == 4            # straight category
    assert eval5(wheel) < eval5(six_high)


def test_best_picks_five_of_seven():
    # Board: A K Q J 2 of mixed suits; hole: T 3 -> should find the Broadway straight.
    board = [card(12, 0), card(11, 1), card(10, 2), card(9, 3), card(0, 0)]
    hole = [card(8, 1), card(1, 2)]
    score = best(hole + board)
    assert score[0] == 4                    # straight
    assert score[1] == 12                   # ace-high


def test_flush_beats_straight():
    flush = [card(r, 0) for r in (2, 4, 6, 8, 10)]
    straight = [card(4, 0), card(5, 1), card(6, 2), card(7, 3), card(8, 0)]
    assert eval5(flush)[0] == 5
    assert eval5(straight)[0] == 4
    assert eval5(flush) > eval5(straight)

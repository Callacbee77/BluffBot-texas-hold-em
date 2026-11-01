"""Equity / draw / blocker signal checks. Loose bounds - Monte Carlo, not exact."""

from bluffbot.cards import cstr
from bluffbot.evaluator import blocker_score, draw_prob, equity


def card(rank, suit):
    return suit * 13 + rank


def test_aces_have_high_equity_preflop():
    aces = [card(12, 0), card(12, 1)]
    eq = equity(aces, [], sims=400)
    assert eq >= 0.75


def test_seven_deuce_offsuit_is_weak_preflop():
    trash = [card(5, 0), card(0, 1)]   # 7♠ 2♥
    eq = equity(trash, [], sims=400)
    assert eq <= 0.45


def test_made_hand_has_no_draw_prob():
    # Already a flush on the flop -> draw_prob is 0 (nothing left to draw to).
    hole = [card(12, 0), card(11, 0)]
    board = [card(9, 0), card(5, 0), card(2, 0)]
    assert draw_prob(hole, board) == 0.0


def test_flush_draw_has_positive_draw_prob():
    hole = [card(12, 0), card(7, 0)]
    board = [card(9, 0), card(5, 0), card(2, 1)]
    assert draw_prob(hole, board) > 0.10


def test_ace_of_flush_suit_is_a_full_blocker():
    # Board has three spades, hole holds the A♠ -> full blocker.
    hole = [card(12, 0), card(3, 1)]
    board = [card(9, 0), card(5, 0), card(2, 0)]
    assert blocker_score(hole, board) == 1.0


def test_no_suit_on_board_means_no_blocker():
    hole = [card(12, 0), card(11, 0)]
    board = [card(9, 0), card(5, 1), card(2, 2)]
    assert blocker_score(hole, board) == 0.0

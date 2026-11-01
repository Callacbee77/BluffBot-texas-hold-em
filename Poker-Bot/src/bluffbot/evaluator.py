"""Hand evaluation plus the three signal functions the bot uses:
equity (IDEA 1), draw_prob (IDEA 3), blocker_score (IDEA 4).
No dependency on the bot or the engine - this module is pure."""

import itertools
import random
from collections import Counter


def eval5(cs):
    """Score a 5-card hand as a comparable tuple (higher is better)."""
    rs = sorted((c % 13 for c in cs), reverse=True)
    flush = len({c // 13 for c in cs}) == 1
    cnt = Counter(rs)
    groups = sorted(cnt.items(), key=lambda x: (x[1], x[0]), reverse=True)
    uniq = sorted(cnt, reverse=True)
    sh = None
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            sh = uniq[0]
        elif uniq == [12, 3, 2, 1, 0]:
            sh = 3  # wheel
    shape = [g[1] for g in groups]
    order = [g[0] for g in groups]
    if sh is not None and flush: return (8, sh)
    if shape == [4, 1]: return (7, *order)
    if shape == [3, 2]: return (6, *order)
    if flush: return (5, *rs)
    if sh is not None: return (4, sh)
    if shape == [3, 1, 1]: return (3, *order)
    if shape == [2, 2, 1]: return (2, *order)
    if shape == [2, 1, 1, 1]: return (1, *order)
    return (0, *rs)


def best(cs):
    """Best 5-card score from up to 7 cards."""
    return max(eval5(c) for c in itertools.combinations(cs, 5))


# IDEA 1: equity by Monte-Carlo simulation
def equity(hole, board, sims=120):
    """Win-rate vs a uniformly random opponent hand over `sims` deals."""
    dead = set(hole) | set(board)
    deck = [c for c in range(52) if c not in dead]
    need = 5 - len(board)
    score = 0.0
    for _ in range(sims):
        s = random.sample(deck, 2 + need)
        opp, full = s[:2], board + s[2:]
        a, b = best(hole + full), best(opp + full)
        score += 1 if a > b else 0.5 if a == b else 0
    return score / sims


# IDEA 3: draw detection (semi-bluff fuel)
def draw_prob(hole, board):
    """Chance the next card makes us a straight-or-better (when we aren't already)."""
    if len(board) not in (3, 4):
        return 0.0
    if best(hole + board)[0] >= 4:
        return 0.0
    dead = set(hole) | set(board)
    unseen = [c for c in range(52) if c not in dead]
    hits = sum(1 for c in unseen if best(hole + board + [c])[0] >= 4)
    return hits / len(unseen)


# IDEA 4: blockers
def blocker_score(hole, board):
    """1.0 if we hold the A/K of a suit with 3+ cards on board (blocks the nut flush)."""
    if len(board) < 3:
        return 0.0
    suit, n = Counter(c // 13 for c in board).most_common(1)[0]
    if n < 3:
        return 0.0
    mine = [c % 13 for c in hole if c // 13 == suit]
    if not mine:
        return 0.0
    return 1.0 if max(mine) >= 11 else 0.5

"""Heads-up game engine: deals, runs the betting loop, settles the pot.
Blinds 10/20, max 3 raises per street."""

import random

from .bot import BluffBot
from .cards import cstr
from .evaluator import best


def play_hand(agents, stacks, button, sb=10, bb=20, log=lambda *a: None):
    deck = list(range(52))
    random.shuffle(deck)
    holes = [[deck.pop(), deck.pop()] for _ in range(2)]
    board, stacks, pot = [], list(stacks), 0
    start = list(stacks)
    for a in agents:
        a.notes = [] if isinstance(a, BluffBot) else a.notes

    def pay(i, amt):
        amt = max(0, min(amt, stacks[i]))
        stacks[i] -= amt
        return amt

    def betting(first, c, street):
        cur, acted, raises, last = first, [False, False], 0, None
        while True:
            if c[0] == c[1] and (all(acted) or 0 in stacks):
                return None
            tc = c[1 - cur] - c[cur]
            view = dict(hole=holes[cur], board=board[:], pot=pot + sum(c), to_call=tc,
                        stack=stacks[cur], opp_stack=stacks[1 - cur],
                        raises_left=3 - raises, street=street, bb=bb)
            kind, x = agents[cur].act(view)
            if last is not None and last != cur:
                cb = getattr(agents[last], "saw_response", None)
                if cb:
                    cb(kind == "fold" and tc > 0)
                last = None
            if kind == "fold" and tc > 0:
                log(f"  {agents[cur].name} folds")
                return 1 - cur
            if kind == "bet":
                cap = min(c[1 - cur] + stacks[1 - cur] - (c[cur] + tc), stacks[cur] - tc)
                x = min(x, cap)
                if x <= 0 or raises >= 3:
                    kind = "call"
                else:
                    x = max(x, min(bb, cap))
                    c[cur] += pay(cur, tc + x)
                    acted = [False, False]
                    acted[cur] = True
                    raises += 1
                    last = cur
                    log(f"  {agents[cur].name} {'raises' if tc else 'bets'} {x}")
                    cur = 1 - cur
                    continue
            c[cur] += pay(cur, tc)
            acted[cur] = True
            log(f"  {agents[cur].name} {'calls ' + str(tc) if tc else 'checks'}")
            cur = 1 - cur

    sbi = button
    c = [0, 0]
    c[sbi], c[1 - sbi] = pay(sbi, sb), pay(1 - sbi, bb)
    winner = None
    for street, ncards in enumerate([0, 3, 1, 1]):
        if street:
            board += [deck.pop() for _ in range(ncards)]
            log(f"\n-- {['','Flop','Turn','River'][street]}: {' '.join(cstr(x) for x in board)}")
            c = [0, 0]
        winner = betting(sbi if street == 0 else 1 - sbi, c, street)
        pot += sum(c)
        if winner is not None:
            break
    if winner is None:
        a, b = best(holes[0] + board), best(holes[1] + board)
        log(f"\nShowdown: {agents[0].name} {' '.join(cstr(x) for x in holes[0])}  vs  "
            f"{agents[1].name} {' '.join(cstr(x) for x in holes[1])}")
        if a > b: stacks[0] += pot
        elif b > a: stacks[1] += pot
        else: stacks[0] += pot // 2; stacks[1] += pot - pot // 2
    else:
        stacks[winner] += pot
    return stacks, [stacks[i] - start[i] for i in range(2)], holes

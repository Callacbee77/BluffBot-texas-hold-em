"""The BluffBot agent. Implements the decision policy: value bet / check / bluff,
plus the fold/call/raise branch when facing a bet. See docs/how-the-bluffing-works.md."""

import random

from .evaluator import blocker_score, draw_prob, equity


class BluffBot:
    name = "BluffBot"

    def __init__(self, sims=120, bet_frac=0.75):
        self.sims, self.bet_frac = sims, bet_frac
        self.value_bets = self.bluffs = 0
        self.bluff_wins = 0          # bluffs that made the opponent fold
        self.opp_folds = self.opp_responses = 0
        self.pending = None
        self.notes = []

    # IDEA 5: opponent model (Laplace-smoothed fold rate, prior ~40%)
    def fold_rate(self):
        return (self.opp_folds + 2) / (self.opp_responses + 5)

    def saw_response(self, folded):
        self.opp_responses += 1
        self.opp_folds += int(folded)
        if folded and self.pending == "bluff":
            self.bluff_wins += 1
        self.pending = None

    def act(self, v):
        hole, board, pot = v["hole"], v["board"], v["pot"]
        tc, raises_left = v["to_call"], v["raises_left"]
        eq = equity(hole, board, self.sims)
        draw, blk = draw_prob(hole, board), blocker_score(hole, board)

        size = max(v["bb"], round(self.bet_frac * pot))
        b = size / pot
        target = b / (1 + 2 * b)                       # IDEA 2: GTO bluff share of betting range
        n = self.value_bets + self.bluffs
        share = self.bluffs / n if n else 0.0
        f = self.fold_rate()
        total = tc + size                              # chips we'd put in
        eq_called = min(0.5, eq * 0.8 + draw * 0.5)    # when called we're usually behind
        ev = f * pot + (1 - f) * (eq_called * (pot + total) - (1 - eq_called) * total)
        quality = min(1.0, 0.25 + 2 * draw + 0.4 * blk)  # how good a bluff candidate is this hand
        info = (f"eq={eq:.2f} draw={draw:.2f} blocker={blk:.1f} | opp folds {f:.0%}, "
                f"bluff share {share:.0%} (target {target:.0%}), bluff EV {ev:+.0f}")

        def bet(kind, why):
            if kind == "bluff":
                self.bluffs += 1
            else:
                self.value_bets += 1
            self.pending = kind
            self.notes.append(
                f"{['preflop','flop','turn','river'][v['street']]}: "
                f"{kind.upper()} {size} - {why} [{info}]"
            )
            return ("bet", size)

        def other(act, why):
            self.notes.append(
                f"{['preflop','flop','turn','river'][v['street']]}: {act} - {why} [{info}]"
            )

        if tc == 0:
            if eq >= 0.68:
                return bet("value", "strong hand, bet for value")
            if eq < 0.45 and ev > 0 and (share < target or f > 0.55) and random.random() < quality:
                why = ("semi-bluff: draw can still improve" if draw > 0.15 else
                       "blocker bluff: I hold the key flush card" if blk >= 1 else
                       "pure bluff: bluff share is under target and +EV")
                return bet("bluff", why)
            other("check", "not strong enough to value-bet, not a good/+EV bluff spot")
            return ("call", 0)

        need = tc / (pot + tc)  # equity needed to call profitably
        if eq >= 0.85 and raises_left > 0:
            return bet("value", "monster, raise for value")
        if draw >= 0.25 and eq < 0.5 and ev > 0 and raises_left > 0 and random.random() < 0.3:
            return bet("bluff", "semi-bluff raise with a big draw")
        if eq >= need + 0.03:
            other("call", f"equity {eq:.2f} beats pot odds {need:.2f}")
            return ("call", 0)
        if eq >= need - 0.08 and random.random() < 0.35:
            other("call", "close to pot odds; occasional bluff-catch so I can't be bluffed freely")
            return ("call", 0)
        other("fold", f"equity {eq:.2f} below pot odds {need:.2f}")
        return ("fold", 0)

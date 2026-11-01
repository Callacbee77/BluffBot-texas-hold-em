"""Opponent agents used by --selfplay and by the human-play mode."""

from .cards import cstr
from .evaluator import equity


class Station:
    """Never folds, never bets. Bluffing into it is pointless."""
    name = "CallingStation"
    notes = []

    def act(self, v):
        return ("call", 0)


class Nit:
    """Only continues with strong hands. Bluffing into it is gold."""
    name = "Nit"
    notes = []

    def act(self, v):
        eq = equity(v["hole"], v["board"], 60)
        if v["to_call"] > 0:
            return ("call", 0) if eq > 0.75 else ("fold", 0)
        return ("bet", round(0.6 * v["pot"])) if eq > 0.75 else ("call", 0)


class Human:
    name = "You"
    notes = []

    def act(self, v):
        print(f"\n  Board: {' '.join(cstr(c) for c in v['board']) or '(preflop)'}   Your hand: "
              f"{' '.join(cstr(c) for c in v['hole'])}")
        print(f"  Pot {v['pot']}  | to call {v['to_call']} | your stack {v['stack']}")
        while True:
            s = input("  [f]old  [c]heck/call  [b <amount>] bet/raise  [q]uit > ").strip().lower().split()
            if not s:
                continue
            if s[0] == "q":
                raise SystemExit
            if s[0] == "f":
                return ("fold", 0)
            if s[0] == "c":
                return ("call", 0)
            if s[0] in ("b", "r"):
                try:
                    return ("bet", int(s[1]) if len(s) > 1 else v["bb"] * 2)
                except ValueError:
                    pass

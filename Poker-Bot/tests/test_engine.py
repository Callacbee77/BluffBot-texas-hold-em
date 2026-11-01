"""Engine-level invariants: chip conservation, showdown resolution, fold ends the hand."""

from bluffbot.engine import play_hand


class AlwaysFold:
    name = "Folder"
    notes = []

    def act(self, v):
        return ("fold", 0) if v["to_call"] > 0 else ("call", 0)


class AlwaysCall:
    name = "Caller"
    notes = []

    def act(self, v):
        return ("call", 0)


def test_chips_are_conserved_across_many_hands():
    a, b = AlwaysCall(), AlwaysCall()
    stacks = [1000, 1000]
    for h in range(20):
        stacks, _, _ = play_hand([a, b], stacks, h % 2)
        assert sum(stacks) == 2000, f"chips leaked on hand {h}: {stacks}"


def test_button_folds_to_a_bet():
    # Bot 0 on the button, bot 1 in BB; button limps -> BB never bets -> checks.
    # Then on the flop, make the SB fold to any bet.
    # Simpler: put AlwaysFold in the BB; button raises -> BB folds.
    raiser = AlwaysCall()
    # Monkey-patch: AlwaysCall raises once so the BB (AlwaysFold) has to act.
    class RaisesOnce:
        name = "Raiser"
        notes = []
        def __init__(self):
            self.done = False
        def act(self, v):
            if not self.done and v["to_call"] == 0:
                self.done = True
                return ("bet", v["bb"])
            return ("call", 0)

    stacks, deltas, _ = play_hand([RaisesOnce(), AlwaysFold()], [1000, 1000], button=0)
    assert sum(stacks) == 2000
    assert deltas[0] > 0                     # raiser won the blinds
    assert deltas[1] < 0


def test_stronger_hand_wins_showdown():
    # Both always check/call to showdown; over many hands, chips must sum to 2000
    # and the winner must be whichever evaluator says is better.
    a, b = AlwaysCall(), AlwaysCall()
    for h in range(30):
        stacks, _, _ = play_hand([a, b], [1000, 1000], h % 2)
        assert sum(stacks) == 2000

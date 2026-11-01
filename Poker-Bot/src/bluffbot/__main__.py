"""Entry point: `python -m bluffbot` or the `bluffbot` console script."""

import argparse

from .bot import BluffBot
from .cards import cstr
from .engine import play_hand
from .opponents import Human, Nit, Station


def selfplay(n, sims):
    for opp in (Station(), Nit()):
        bot = BluffBot(sims)
        net = 0
        for h in range(n):
            _, d, _ = play_hand([bot, opp], [1000, 1000], h % 2)
            net += d[0]
        tot = bot.bluffs + bot.value_bets
        print(f"vs {opp.name:15s} net {net:+6d} chips in {n} hands | bets: {tot} "
              f"(bluffs {bot.bluffs} = {bot.bluffs / max(1, tot):.0%}, "
              f"{bot.bluff_wins} of them won by fold) | learned fold-rate {bot.fold_rate():.0%}")


def play_human(sims):
    bot, me = BluffBot(sims), Human()
    stacks, button, hand = [1000, 1000], 0, 0   # index 0 = bot, 1 = you
    while min(stacks) >= 20:
        hand += 1
        print(f"\n{'=' * 50}\nHand {hand} | stacks: bot {stacks[0]}, you {stacks[1]} | "
              f"{'bot' if button == 0 else 'you'} on the button")
        stacks, _, holes = play_hand([bot, me], stacks, button, log=print)
        print(f"\n  Bot held {' '.join(cstr(x) for x in holes[0])}. Bot's thinking this hand:")
        for note in bot.notes:
            print("   *", note)
        button = 1 - button
    print("\nGame over!", "You win!" if stacks[1] > stacks[0] else "Bot wins!")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="bluffbot",
                                 description="Heads-up Texas Hold'em bot built around bluffing.")
    ap.add_argument("--selfplay", type=int, metavar="N",
                    help="run N hands vs a calling station and a nit, print net chips")
    ap.add_argument("--sims", type=int, default=120,
                    help="Monte-Carlo simulations per decision (default 120)")
    a = ap.parse_args(argv)
    if a.selfplay:
        selfplay(a.selfplay, a.sims)
    else:
        play_human(a.sims)


if __name__ == "__main__":
    main()

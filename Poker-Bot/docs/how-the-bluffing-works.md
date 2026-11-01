# How the bluffing works

![BluffBot decision flowchart](assets/bluffing-flowchart.png)

The diagram above shows what the bot does when it can bet. It combines five ideas:

## 1. Equity

The bot deals out the rest of the hand against random opponent hands about 120
times and counts how often it wins. That one number tells it whether to
value-bet, check, or consider a bluff.

## 2. Bluff ratio (balance)

If you bet size `B` into a pot of size `P`, game theory says the share of your
bets that are bluffs should be about `B / (P + 2B)`. Betting 75% of the pot
gives about 30% bluffs. The bot tracks its own bluff-to-value ratio and only
bluffs when it is under that target. Too few bluffs and you never get paid on
strong hands; too many and you get called down.

## 3. Semi-bluffs

The best bluffs are hands that are behind now but can still improve. The bot
counts how many next cards would give it a straight or better. A flush-draw
bluff that gets called can still win, so draws get picked more often as bluff
candidates.

## 4. Blockers

If the board has three of one suit and the bot holds the ace or king of that
suit, you are less likely to have the nut flush. That makes you fold more, so
the bot treats this as a better bluff spot.

## 5. Exploiting you

The bot keeps a running count of how often you fold when it bets, starting
from a guess of 40%. It then computes the expected value of a bluff as:

```
EV = fold% × pot + (1 − fold%) × (what happens when called)
```

If that is zero or negative, it stops bluffing. If you fold a lot, it bluffs
more — even above the 30% target.

## The bluff gate

The "bluff gate" in the diagram requires **three checks to pass**:

1. **Ratio** — its bluff share is under target, or you fold more than 55% of the time.
2. **EV** — the bluff has positive expected value.
3. **Quality roll** — a random roll weighted toward draws and blockers comes up.

## When you bet into it

The bot calls if its equity beats the pot odds, with a small chance of calling
slightly below them. It sometimes raises big draws as a bluff and re-raises
monsters for value.

## Caveats

This is a **simplified bot, not a solver**. It uses one bet size, equity
against a random hand rather than a modeled range, and a basic opponent model.
A natural next step is to give it multiple bet sizes, or to have it estimate
what hands you would bet in each spot.

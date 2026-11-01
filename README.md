# BluffBot

> A heads-up Texas Hold'em bot that thinks out loud about when to bluff.

**BluffBot** is a heads-up Texas Hold'em bot written in pure Python (no
runtime dependencies) built around a single thesis: **bluffing is not
gambling, it's a calculation.** Every bet it makes traces back to one of five
interlocking ideas.

![BluffBot decision flowchart](docs/assets/bluffing-flowchart.png)

## The five ideas

1. **Equity** — deals the rest of the hand against a random opponent ~120 times per decision; that number decides value-bet / check / consider-bluff.
2. **Balance** — tracks its own bluff-to-value ratio and only bluffs when under the GTO target `B / (P + 2B)` (~30% at ¾ pot).
3. **Semi-bluffs** — draws get picked as bluff candidates because they can still win when called.
4. **Blockers** — holding the ace/king of a three-suited board makes the opponent fold more, so it's a better bluff spot.
5. **Exploitation** — learns your fold rate and computes the EV of a bluff; if EV goes negative it stops bluffing, and if you fold a lot it bluffs more.

A bluff only fires when **three gates** pass: the ratio gate, the EV gate, and
a quality roll weighted toward draws and blockers. Details in
[`docs/how-the-bluffing-works.md`](docs/how-the-bluffing-works.md).

## Quickstart

```bash
git clone https://github.com/<you>/bluff

"""BluffBot - a heads-up Texas Hold'em bot built around bluffing."""

from .bot import BluffBot
from .cards import cstr
from .engine import play_hand
from .evaluator import best, blocker_score, draw_prob, equity
from .opponents import Human, Nit, Station

__all__ = [
    "BluffBot", "Human", "Nit", "Station",
    "best", "blocker_score", "cstr", "draw_prob", "equity", "play_hand",
]

__version__ = "0.1.0"

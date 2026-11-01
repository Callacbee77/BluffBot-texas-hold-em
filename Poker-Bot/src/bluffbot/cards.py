"""Card constants and formatting. No dependencies on any other module."""

RANKS = "23456789TJQKA"
SUITS = "♠♥♦♣"


def cstr(c: int) -> str:
    """Render a card integer (0..51) as e.g. 'A♠' or '7♦'."""
    return RANKS[c % 13] + SUITS[c // 13]

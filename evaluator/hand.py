"""
hand.py

Defines classes for representing cards and poker hands.
"""

from typing import List

SUITS = 'shdc'  # spades, hearts, diamonds, clubs
RANKS = '23456789TJQKA' #2-Ace

class Card:
    def __init__(self, rank: str, suit: str):
        assert rank in RANKS, f"Invalid rank: {rank}"
        assert suit in SUITS, f"Invalid suit: {suit}"
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    @staticmethod
    def from_str(card_str: str):
        assert len(card_str) == 2, "Card string must be 2 characters"
        return Card(card_str[0], card_str[1])

class Hand:
    def __init__(self, cards: List[Card]):
        assert len(cards) in [2, 5, 7], "Hand must have 2, 5, or 7 cards"
        self.cards = cards

    def __repr__(self):
        return " ".join(str(card) for card in self.cards)
"""
hand.py

Defines classes for representing cards and poker hands used in Texas Hold'em.

- Card: Represents a single playing card with a rank (e.g., 'A', 'K', '2') and a suit ('s', 'h', 'd', 'c').
  - Validates input rank and suit
  - Can be printed (e.g., 'As' for Ace of Spades)
  - Supports creation from string via Card.from_str('Ah')

- Hand: Represents a poker hand (5 or 7 cards).
  - Use Hand.seven_card_hand() or Hand.five_card_hand() to enforce length.
  - Provides a readable string representation of the hand

These classes are used by the evaluator module to analyze and compare hands.
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
        self.cards = cards

    @classmethod
    def seven_card_hand(cls, cards: List[Card]):
        assert len(cards) == 7, "Hand must have exactly 7 cards (Texas Hold'em showdown)"
        return cls(cards)

    @classmethod
    def five_card_hand(cls, cards: List[Card]):
        assert len(cards) == 5, "Hand must have exactly 5 cards"
        return cls(cards)

    def __repr__(self):
        return " ".join(str(card) for card in self.cards)
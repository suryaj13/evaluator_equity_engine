"""
evaluator.py

Evaluates and ranks poker hands.
"""

from .hand import Card, Hand

HAND_RANKS = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind",
    "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
]

RANK_ORDER = {r: i for i, r in enumerate('23456789TJQKA', start=2)}

def evaluate_hand(hand: Hand) -> int:
    """
    Returns an integer representing the hand's rank.
    0 = High Card, 1 = One Pair, ..., 8 = Straight Flush
    """
    # Placeholder: always returns High Card
    # TODO: Implement real hand evaluation logic
    return 0

def classify_hand(hand: Hand) -> str:
    """
    Returns a string describing the hand's rank.
    """
    rank = evaluate_hand(hand)
    return HAND_RANKS[rank]

def hand_strength(hand: Hand):
    """
    Returns a tuple (hand_rank, [sorted_ranks]) for tie-breaking.
    Higher tuple means a stronger hand.
    """
    # Placeholder: only works for high card
    # TODO: Implement logic for all hand types
    hand_rank = evaluate_hand(hand)
    # Sort card ranks descending for kicker comparison
    sorted_ranks = sorted([RANK_ORDER[c.rank] for c in hand.cards], reverse=True)
    return (hand_rank, sorted_ranks)

def compare_hands(hand1: Hand, hand2: Hand) -> int:
    """
    Compares two hands.
    Returns:
        1 if hand1 wins,
        -1 if hand2 wins,
        0 if tie.
    """
    strength1 = hand_strength(hand1)
    strength2 = hand_strength(hand2)
    if strength1 > strength2:
        return 1
    elif strength1 < strength2:
        return -1
    else:
        return 0
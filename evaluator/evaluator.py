"""
evaluator.py

Evaluates and ranks poker hands.
"""
from collections import Counter
from .hand import Card, Hand


HAND_RANKS = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind",
    "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
]

RANK_ORDER = {r: i for i, r in enumerate('23456789TJQKA', start=2)}

# NOTE: This function evaluates a 5-card poker hand and returns a numerical rank from 0 to 8,
# where 0 = High Card and 8 = Straight Flush.
#
# 🔍 Step-by-step breakdown:
# 1. Extract the ranks and suits of all 5 cards.
# 2. Convert ranks into numeric values using RANK_ORDER (e.g., 'A' → 14, 'K' → 13).
# 3. Check for Ace-low straight by also considering Ace as 1 (for A-2-3-4-5).
# 4. Determine if the hand is a flush by checking if all suits are the same.
# 5. Determine if the hand is a straight by checking for 5 consecutive values.
# 6. Use a Counter to count how many times each rank appears.
# 7. Use frequency patterns (like [3,2] for Full House, or [2,2,1] for Two Pair)
#    to classify the hand.
# 8. Return the corresponding hand rank index:
#     - 8: Straight Flush
#     - 7: Four of a Kind
#     - 6: Full House
#     - 5: Flush
#     - 4: Straight
#     - 3: Three of a Kind
#     - 2: Two Pair
#     - 1: One Pair
#     - 0: High Card
#
# This function does NOT handle tie-breaking logic (use hand_strength for that).

def evaluate_hand(hand: Hand) -> int:
    ranks = [card.rank for card in hand.cards]
    suits = [card.suit for card in hand.cards]

    # Convert ranks to values using RANK_ORDER
    values = sorted([RANK_ORDER[r] for r in ranks], reverse=True)
    
    # Handle Ace-low straight (e.g. A-2-3-4-5)
    alt_values = set(values)
    if 14 in alt_values:  # Ace present
        alt_values.add(1)

    def is_consecutive(vals):
        return all(vals[i] - 1 == vals[i+1] for i in range(len(vals) - 1))

    is_flush = len(set(suits)) == 1
    is_straight = is_consecutive(values) or is_consecutive(sorted(alt_values, reverse=True))

    rank_counts = Counter(ranks)
    count_values = sorted(rank_counts.values(), reverse=True)

    if is_flush and is_straight:
        return 8  # Straight Flush
    elif count_values == [4, 1]:
        return 7  # Four of a Kind
    elif count_values == [3, 2]:
        return 6  # Full House
    elif is_flush:
        return 5  # Flush
    elif is_straight:
        return 4  # Straight
    elif count_values == [3, 1, 1]:
        return 3  # Three of a Kind
    elif count_values == [2, 2, 1]:
        return 2  # Two Pair
    elif count_values == [2, 1, 1, 1]:
        return 1  # One Pair
    else:
        return 0  # High Card

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
    
hand = Hand([Card('A', 's'), Card('K', 's'), Card('Q', 's'), Card('J', 's'), Card('T', 's')])
print(classify_hand(hand))  # Should print "Straight Flush"
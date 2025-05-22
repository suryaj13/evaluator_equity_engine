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
    values = sorted([RANK_ORDER[r] for r in ranks], reverse=True)

    alt_values = set(values)
    if 14 in alt_values:
        alt_values.add(1)

    def is_consecutive(vals):
        return all(vals[i] - 1 == vals[i+1] for i in range(len(vals) - 1))

    is_flush = len(set(suits)) == 1
    is_straight = is_consecutive(values) or is_consecutive(sorted(alt_values, reverse=True))

    rank_counts = Counter(ranks)
    count_values = sorted(rank_counts.values(), reverse=True)

    if is_flush and is_straight:
        return 8
    elif count_values == [4, 1]:
        return 7
    elif count_values == [3, 2]:
        return 6
    elif is_flush:
        return 5
    elif is_straight:
        return 4
    elif count_values == [3, 1, 1]:
        return 3
    elif count_values == [2, 2, 1]:
        return 2
    elif count_values == [2, 1, 1, 1]:
        return 1
    else:
        return 0

# NOTE: This function maps a hand to its textual classification.
#
# 🧩 Step-by-step breakdown:
# 1. Calls evaluate_hand() to get the numerical hand rank (0 to 8).
# 2. Uses HAND_RANKS[] list to convert the number to a string.
# 3. Returns the corresponding hand name like "Flush", "Two Pair", etc.
#
# This is a simple helper for readability and debugging output.

def classify_hand(hand: Hand) -> str:
    rank_index = evaluate_hand(hand)
    return HAND_RANKS[rank_index]

# NOTE: This function returns a (rank, tiebreaker_values) tuple to compare hands.
#
# 🧠 Step-by-step breakdown:
# 1. Count occurrences of each card rank using Counter.
# 2. Convert ranks to numerical values using RANK_ORDER.
# 3. Sort by frequency first (e.g. trips > pair) and then by rank.
# 4. Build a sorted list of ranks used for tie-breaking.
# 5. Handle special case of A-2-3-4-5 (low straight).
# 6. Return a tuple: (hand rank, list of tiebreakers).
#
# This is what enables proper hand comparison beyond just classifying them.

def hand_strength(hand: Hand):
    rank_counts = Counter(card.rank for card in hand.cards)
    hand_rank = evaluate_hand(hand)

    counts = [(RANK_ORDER[r], c) for r, c in rank_counts.items()]
    sorted_counts = sorted(counts, key=lambda x: (x[1], x[0]), reverse=True)
    sorted_ranks = [r for r, _ in sorted_counts]

    values = sorted([RANK_ORDER[c.rank] for c in hand.cards], reverse=True)
    if set(values) == {14, 2, 3, 4, 5}:
        sorted_ranks = [5]

    if hand_rank in [4, 8]:
        return (hand_rank, [max(sorted_ranks)])
    elif hand_rank == 7:
        return (hand_rank, [sorted_ranks[0], sorted_ranks[1]])
    elif hand_rank == 6:
        return (hand_rank, [sorted_ranks[0], sorted_ranks[1]])
    elif hand_rank in [5, 0]:
        return (hand_rank, sorted_ranks)
    elif hand_rank == 3:
        return (hand_rank, [sorted_ranks[0]] + sorted_ranks[1:])
    elif hand_rank == 2:
        return (hand_rank, [sorted_ranks[0], sorted_ranks[1], sorted_ranks[2]])
    elif hand_rank == 1:
        return (hand_rank, [sorted_ranks[0]] + sorted_ranks[1:])
    else:
        return (hand_rank, sorted_ranks)

# NOTE: This function compares two hands and returns who wins.
#
# ⚔️ Step-by-step breakdown:
# 1. Call hand_strength() on both hands.
# 2. Compare the (rank, tiebreaker) tuples using Python's built-in tuple comparison.
# 3. Return:
#    - 1 if hand1 is stronger,
#    - -1 if hand2 is stronger,
#    - 0 if it's a tie.
#
# This enables use of the engine in head-to-head games.

def compare_hands(hand1: Hand, hand2: Hand) -> int:
    strength1 = hand_strength(hand1)
    strength2 = hand_strength(hand2)
    if strength1 > strength2:
        return 1
    elif strength1 < strength2:
        return -1
    else:
        return 0
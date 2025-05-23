from collections import Counter
from itertools import combinations
from .hand import Card, Hand

HAND_RANKS = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind",
    "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
]
RANK_ORDER = {r: i for i, r in enumerate('23456789TJQKA', start=2)}

def _evaluate_5(cards):
    ranks = [c.rank for c in cards]
    suits = [c.suit for c in cards]
    values = sorted([RANK_ORDER[r] for r in ranks], reverse=True)
    flush = len(set(suits)) == 1
    straight = all(values[i] - 1 == values[i+1] for i in range(4)) or values == [14, 5, 4, 3, 2]
    freq = Counter(ranks)
    count = sorted(freq.values(), reverse=True)
    count_rank = sorted(((c, RANK_ORDER[r]) for r, c in freq.items()), reverse=True)
    tiebreak = [r for c, r in count_rank for _ in range(c)]

    if straight and flush: return (8, [5] if values == [14, 5, 4, 3, 2] else [values[0]])
    if count == [4, 1]: return (7, tiebreak)
    if count == [3, 2]: return (6, tiebreak)
    if flush: return (5, values)
    if straight: return (4, [5] if values == [14, 5, 4, 3, 2] else [values[0]])
    if count == [3, 1, 1]: return (3, tiebreak)
    if count == [2, 2, 1]: return (2, tiebreak)
    if count == [2, 1, 1, 1]: return (1, tiebreak)
    return (0, values)

def best_hand(hand: Hand):
    if len(hand.cards) != 7:
        raise ValueError("Hand must have exactly 7 cards")
    combos = combinations(hand.cards, 5)
    best_combo = max(combos, key=lambda c: _evaluate_5(c))
    return _evaluate_5(best_combo), Hand(list(best_combo))

def classify_hand(hand: Hand) -> str:
    return HAND_RANKS[best_hand(hand)[0][0]]

def hand_strength(hand: Hand):
    return best_hand(hand)[0]

def compare_hands(*hands):
    if len(hands) < 2:
        raise ValueError("compare_hands requires at least two Hand objects")
    scores = [hand_strength(h) for h in hands]
    if len(hands) == 2:
        return 1 if scores[0] > scores[1] else -1 if scores[0] < scores[1] else 0
    max_score = max(scores)
    return [h for h, s in zip(hands, scores) if s == max_score]
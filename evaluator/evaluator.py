from collections import Counter
from itertools import combinations
from .hand import Card, Hand

HAND_RANKS = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind",
    "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
]
RANK_ORDER = {r: i for i, r in enumerate('23456789TJQKA', start=2)}

def _evaluate_combination(hand: Hand):
    ranks = [card.rank for card in hand.cards]
    suits = [card.suit for card in hand.cards]
    values = sorted([RANK_ORDER[r] for r in ranks], reverse=True)
    is_flush = len(set(suits)) == 1
    low_straight = values == [14, 5, 4, 3, 2]
    is_straight = all(values[i] - 1 == values[i+1] for i in range(4)) or low_straight
    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)
    count_rank = sorted(((cnt, RANK_ORDER[rank]) for rank, cnt in rank_counts.items()), reverse=True)
    tiebreak = [rank for cnt, rank in count_rank for _ in range(cnt)]
    if is_straight and is_flush:
        return (8, [5] if low_straight else [values[0]])
    if counts == [4, 1]:
        return (7, tiebreak)
    if counts == [3, 2]:
        return (6, tiebreak)
    if is_flush:
        return (5, values)
    if is_straight:
        return (4, [5] if low_straight else [values[0]])
    if counts == [3, 1, 1]:
        return (3, tiebreak)
    if counts == [2, 2, 1]:
        return (2, tiebreak)
    if counts == [2, 1, 1, 1]:
        return (1, tiebreak)
    return (0, values)

def best_hand(hand: Hand):
    if len(hand.cards) == 7:
        best = None
        best_combo = None
        for combo in combinations(hand.cards, 5):
            score = _evaluate_combination(Hand(list(combo)))
            if best is None or score > best:
                best = score
                best_combo = combo
        return best, Hand(list(best_combo))
    raise ValueError("Hand must have exactly 7 cards")

def classify_hand(hand: Hand) -> str:
    rank, _ = best_hand(hand)[0]
    return HAND_RANKS[rank]

def hand_strength(hand: Hand):
    return best_hand(hand)[0]

def compare_hands(*hands):
    if len(hands) == 2:
        s1, s2 = hand_strength(hands[0]), hand_strength(hands[1])
        return 1 if s1 > s2 else -1 if s1 < s2 else 0
    if len(hands) > 2:
        strengths = [hand_strength(h) for h in hands]
        max_strength = max(strengths)
        return [h for h, s in zip(hands, strengths) if s == max_strength]
    raise ValueError("compare_hands requires at least two Hand objects")
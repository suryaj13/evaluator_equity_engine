import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Evaluator.hand import Card, Hand
from Evaluator.evaluator import classify_hand, compare_hands

def make_hand(cards):
    """ Helper to convert list of (rank, suit) tuples into a Hand object """
    return Hand([Card(rank, suit) for rank, suit in cards])

def test_classify_hand_types():
    print("Testing classify_hand...")
    hands = {
        "straight_flush": make_hand([('A', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('T', 's')]),
        "four_of_a_kind": make_hand([('9', 'c'), ('9', 'd'), ('9', 'h'), ('9', 's'), ('K', 'd')]),
        "full_house": make_hand([('8', 's'), ('8', 'h'), ('8', 'd'), ('K', 's'), ('K', 'h')]),
        "flush": make_hand([('2', 'h'), ('5', 'h'), ('9', 'h'), ('J', 'h'), ('K', 'h')]),
        "straight": make_hand([('9', 's'), ('8', 'd'), ('7', 'h'), ('6', 's'), ('5', 'c')]),
        "three_of_a_kind": make_hand([('4', 'd'), ('4', 'h'), ('4', 's'), ('T', 'c'), ('K', 'd')]),
        "two_pair": make_hand([('A', 'h'), ('A', 'd'), ('5', 'c'), ('5', 's'), ('3', 'h')]),
        "one_pair": make_hand([('J', 'd'), ('J', 'h'), ('7', 'c'), ('4', 's'), ('2', 'd')]),
        "high_card": make_hand([('A', 's'), ('J', 'd'), ('8', 'c'), ('5', 'h'), ('2', 's')])
    }

    expected = {
        "straight_flush": "Straight Flush",
        "four_of_a_kind": "Four of a Kind",
        "full_house": "Full House",
        "flush": "Flush",
        "straight": "Straight",
        "three_of_a_kind": "Three of a Kind",
        "two_pair": "Two Pair",
        "one_pair": "One Pair",
        "high_card": "High Card"
    }

    for name, hand in hands.items():
        result = classify_hand(hand)
        print(f"Hand: {name:16} | Classified as: {result:16} | Expected: {expected[name]}")
        assert result == expected[name], f"{name} failed: got {result}"

def test_compare_hands():
    print("\nTesting compare_hands...")
    hands = {
        "straight_flush": make_hand([('A', 's'), ('K', 's'), ('Q', 's'), ('J', 's'), ('T', 's')]),
        "four_of_a_kind": make_hand([('9', 'c'), ('9', 'd'), ('9', 'h'), ('9', 's'), ('K', 'd')]),
        "full_house": make_hand([('8', 's'), ('8', 'h'), ('8', 'd'), ('K', 's'), ('K', 'h')]),
        "flush": make_hand([('2', 'h'), ('5', 'h'), ('9', 'h'), ('J', 'h'), ('K', 'h')]),
        "straight": make_hand([('9', 's'), ('8', 'd'), ('7', 'h'), ('6', 's'), ('5', 'c')]),
        "three_of_a_kind": make_hand([('4', 'd'), ('4', 'h'), ('4', 's'), ('T', 'c'), ('K', 'd')]),
        "two_pair": make_hand([('A', 'h'), ('A', 'd'), ('5', 'c'), ('5', 's'), ('3', 'h')]),
        "one_pair": make_hand([('J', 'd'), ('J', 'h'), ('7', 'c'), ('4', 's'), ('2', 'd')]),
        "high_card": make_hand([('A', 's'), ('J', 'd'), ('8', 'c'), ('5', 'h'), ('2', 's')])
    }

    tests = [
        ("straight_flush", "four_of_a_kind", 1),
        ("full_house", "flush", 1),
        ("straight", "three_of_a_kind", 1),
        ("two_pair", "one_pair", 1),
        ("high_card", "high_card", 0),
        ("one_pair", "three_of_a_kind", -1)
    ]

    for h1, h2, expected in tests:
        result = compare_hands(hands[h1], hands[h2])
        print(f"Compare: {h1:16} vs {h2:16} | Result: {result} | Expected: {expected}")
        assert result == expected, f"{h1} vs {h2} failed: got {result}"

if __name__ == "__main__":
    test_classify_hand_types()
    test_compare_hands()
    print("\n✅ Manual tests passed")
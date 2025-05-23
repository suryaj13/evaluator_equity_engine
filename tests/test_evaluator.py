import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluator.hand import Card, Hand
from evaluator.evaluator import compare_hands, classify_hand

def generate_shuffled_deck():
    ranks = '23456789TJQKA'
    suits = 'shdc'
    deck = [Card(r, s) for r in ranks for s in suits]
    random.shuffle(deck)
    return deck

def deal(deck, num):
    return [deck.pop() for _ in range(num)]

def print_hand(label, cards):
    print(f"{label}:", " ".join(str(card) for card in cards))

from evaluator.evaluator import classify_hand

def describe_hand(hand):
    # Use evaluator to classify
    try:
        label = classify_hand(hand)
    except:
        label = "Unknown"
    best_five = hand.cards[:5]  # fallback

    if hasattr(hand, 'five_card_hand') and hasattr(hand.five_card_hand, 'cards'):
        best_five = hand.five_card_hand.cards
    return f"{label}: {' '.join(str(card) for card in best_five)}"

def test_x_player_showdown(num_players=3):
    print(f"\n{num_players}-player showdown test...")
    deck = generate_shuffled_deck()

    player_holes = [deal(deck, 2) for _ in range(num_players)]
    board = deal(deck, 5)

    print_hand("Board", board)
    for i, hole in enumerate(player_holes):
        print_hand(f"Player {i+1} hole", hole)

    hands = [Hand(hole + board) for hole in player_holes]
    scores = [0] * num_players

    print("\nPairwise comparisons:")
    for i in range(num_players):
        for j in range(i + 1, num_players):
            result = compare_hands(hands[i], hands[j])
            outcome = "ties" if result == 0 else f"Player {i+1 if result == 1 else j+1} wins"
            print(
                f"Player {i+1} ({describe_hand(hands[i])}) vs "
                f"Player {j+1} ({describe_hand(hands[j])}): {outcome}"
            )
            if result == 1:
                scores[i] += 1
            elif result == -1:
                scores[j] += 1

    winner = scores.index(max(scores))
    print(f"\nWinner: Player {winner+1} with hand: {describe_hand(hands[winner])}")

    print("\nEdge case: identical hands should tie")
    duplicate_hand = Hand(player_holes[0] + board)
    assert compare_hands(hands[0], duplicate_hand) == 0, "Identical hands should tie"
    print("Edge case passed: tie confirmed")

if __name__ == "__main__":
    import sys
    # Allow user to specify number of players via command line, default to 3
    num_players = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    test_x_player_showdown(num_players=num_players)
    print("\n✅ all randomized tests passed")
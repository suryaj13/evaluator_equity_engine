import random
from equity.equity_calc import EquityCalculator
from evaluator.hand import Card

def get_card_input(prompt, used_cards, auto_randomize=False):
    while True:
        if auto_randomize:
            deck = [r + s for r in '23456789TJQKA' for s in 'shdc']
            available = [c for c in deck if c not in used_cards]
            if not available:
                print("No cards left to randomize!")
                continue
            card_str = random.choice(available)
            print(f"  Randomly selected: {card_str}")
        else:
            card_str = input(prompt).strip()
            if card_str.lower() == 'r':
                auto_randomize = True
                continue
        if len(card_str) == 2 and card_str[0] in '23456789TJQKA' and card_str[1] in 'shdc' and card_str not in used_cards:
            used_cards.add(card_str)
            return card_str
        print("Invalid or duplicate card. Enter as 'As', 'Td', etc. or 'r' to randomize.")

def get_hand_input(player_name, used_cards):
    print(f"\n{player_name}: Choose hand input method:")
    print("  1. Enter cards manually (e.g., As Kh)")
    print("  2. Randomize hand")
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            c1 = get_card_input(f"  Enter first card for {player_name}: ", used_cards)
            c2 = get_card_input(f"  Enter second card for {player_name}: ", used_cards)
            return [c1, c2]
        elif choice == '2':
            c1 = get_card_input("", used_cards, auto_randomize=True)
            c2 = get_card_input("", used_cards, auto_randomize=True)
            return [c1, c2]
        else:
            print("Invalid choice. Enter 1 or 2.")

def get_board_input(stage, num_cards, used_cards):
    print(f"\n{stage}: Choose input method:")
    print(f"  1. Enter {num_cards} card(s) manually")
    print(f"  2. Randomize {num_cards} card(s)")
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            cards = []
            for i in range(num_cards):
                c = get_card_input(f"  Enter card {i+1} for {stage}: ", used_cards)
                cards.append(c)
            return cards
        elif choice == '2':
            cards = []
            for i in range(num_cards):
                c = get_card_input("", used_cards, auto_randomize=True)
                cards.append(c)
            return cards
        else:
            print("Invalid choice. Enter 1 or 2.")

def print_equity(equity, stage, num_players, river=False):
    print(f"\nEquity after {stage}:")
    if river:
        winners = [i for i, eq in enumerate(equity) if abs(eq - max(equity)) < 1e-6]
        if len(winners) == 1:
            print(f"  Winner: {'Hero' if winners[0] == 0 else f'Villain {winners[0]}'} (100.00%)")
        else:
            share = 100.0 / len(winners)
            print(f"  Split pot between: ", end="")
            print(", ".join(["Hero" if i == 0 else f"Villain {i}" for i in winners]), end=" ")
            print(f"({share:.2f}% each)")
    else:
        for i, eq in enumerate(equity):
            label = "Hero" if i == 0 else f"Villain {i}"
            print(f"  {label}: {eq:.2f}%")

def print_final_summary(hero_hand, villain_hands, board, equity_progression):
    print("\n===== FINAL SUMMARY =====")
    print(f"Board: {' '.join(board)}")
    print(f"Hero: {' '.join(hero_hand)}")
    for i, vhand in enumerate(villain_hands):
        print(f"Villain {i+1}: {' '.join(vhand)}")
    print("\nEquity progression:")
    stages = ["Preflop", "Flop", "Turn", "River"]
    for idx, eqs in enumerate(equity_progression):
        print(f"{stages[idx]}:")
        for i, eq in enumerate(eqs):
            label = "Hero" if i == 0 else f"Villain {i}"
            print(f"  {label}: {eq:.2f}%")
    print("========================\n")

def print_equity_explanation():
    print("""
How equity is calculated at each stage:
- Preflop, Flop, Turn: Monte Carlo simulation runs thousands of times, dealing random remaining community cards, and averages the results. Each player's equity is the percentage of the pot they would win or split over all simulations.
- River: With all 5 board cards known, only one simulation is run. The actual winner(s) get 100% (or split if tie).
    """)

def main():
    print("\n♠️ Texas Hold'em Interactive Equity Calculator ♠️\n")
    print_equity_explanation()
    used_cards = set()
    calc = EquityCalculator()
    equity_progression = []

    # Hero hand
    hero_hand = get_hand_input("Hero", used_cards)

    # Number of opponents
    while True:
        try:
            num_villains = int(input("\nEnter number of opponents (1-8): ").strip())
            if 1 <= num_villains <= 8:
                break
        except ValueError:
            pass
        print("Invalid number. Enter an integer between 1 and 8.")

    # Villain hands
    villain_hands = []
    for i in range(num_villains):
        villain_hands.append(get_hand_input(f"Villain {i+1}", used_cards))

    # Preflop equity
    equity = calc.calculate_equity(hero_hand, villain_hands, board=None, num_simulations=5000)
    equity_progression.append(equity)
    print_equity(equity, "preflop", num_villains+1)

    # Flop
    flop = get_board_input("Flop", 3, used_cards)
    equity = calc.calculate_equity(hero_hand, villain_hands, board=flop, num_simulations=5000)
    equity_progression.append(equity)
    print_equity(equity, "flop", num_villains+1)

    # Turn
    turn = get_board_input("Turn", 1, used_cards)
    board_turn = flop + turn
    equity = calc.calculate_equity(hero_hand, villain_hands, board=board_turn, num_simulations=5000)
    equity_progression.append(equity)
    print_equity(equity, "turn", num_villains+1)

    # River
    river = get_board_input("River", 1, used_cards)
    board_river = board_turn + river
    # On the river, only one simulation is needed (no randomness left)
    equity = calc.calculate_equity(hero_hand, villain_hands, board=board_river, num_simulations=1)
    equity_progression.append(equity)
    print_equity(equity, "river", num_villains+1, river=True)

    print_final_summary(hero_hand, villain_hands, board_river, equity_progression)
    print("Thank you for using the interactive equity calculator!\n")

if __name__ == "__main__":
    main() 
import random
from typing import List, Optional, Tuple, Dict
from collections import Counter
from evaluator.hand import Card, Hand
from evaluator.evaluator import hand_strength, compare_hands
from board_setup.board_setup import BoardSetup

class EquityCalculator:
    def __init__(self):
        """
        Initialize the equity calculator.
        """
        self.board_setup = BoardSetup()

    def _evaluate_hands_and_winners(self,
                                  hero_cards: List[Card],
                                  villain_cards: List[Card],
                                  board: List[Card]) -> Dict[int, float]:
        """
        Evaluate all hands and determine winners with pot shares.
        
        Args:
            hero_cards: Hero's hole cards
            villain_cards: List of all villain cards
            board: Complete board
            
        Returns:
            Dictionary mapping player indices to their pot shares
        """
        # Create and evaluate all hands
        all_hands = []
        hero_hand = Hand(hero_cards + board)
        all_hands.append(hero_hand)
        
        # Create villain hands
        for i in range(0, len(villain_cards), 2):
            villain_hand = Hand(villain_cards[i:i+2] + board)
            all_hands.append(villain_hand)
            
        # Get hand strengths
        hand_scores = [hand_strength(h) for h in all_hands]
            
        # Find winners
        max_score = max(hand_scores)
        winners = [i for i, score in enumerate(hand_scores) if score == max_score]
        
        # Calculate pot shares (equal split among winners)
        pot_share = 1.0 / len(winners)
        return {winner: pot_share for winner in winners}

    def calculate_equity(self, 
                        hero_cards: List[str],
                        villain_ranges: List[List[str]],
                        board: Optional[List[str]] = None,
                        num_simulations: int = 10000) -> List[float]:
        """
        Calculate equity using Monte Carlo simulation.
        
        Args:
            hero_cards: List of two cards for the hero (e.g., ["As", "Kh"])
            villain_ranges: List of possible hand ranges for villains
            board: Current board cards (None for preflop)
            num_simulations: Number of Monte Carlo simulations to run
        
        Returns:
            List of equity percentages for each player
            
        Raises:
            ValueError: If inputs are invalid (duplicate cards, invalid format, wrong board length)
        """
        # Validate input lengths
        if len(hero_cards) != 2:
            raise ValueError("Hero must have exactly 2 cards")
        if board and len(board) not in [3, 4, 5]:
            raise ValueError("Board must have 3 (flop), 4 (turn), or 5 (river) cards")
            
        # Convert inputs to Card objects and validate format
        try:
            hero_cards = [Card.from_str(c) for c in hero_cards]
            board = [Card.from_str(c) for c in board] if board else []
            villain_cards = []
            for villain_range in villain_ranges:
                if len(villain_range) != 2:
                    raise ValueError("Each villain must have exactly 2 cards")
                villain_cards.extend([Card.from_str(c) for c in villain_range])
        except (AssertionError, ValueError) as e:
            raise ValueError(f"Invalid card format: {str(e)}")
            
        # Check for duplicate cards
        all_cards = hero_cards + board + villain_cards
        card_strs = [(c.rank + c.suit) for c in all_cards]
        if len(set(card_strs)) != len(card_strs):
            raise ValueError("Duplicate cards detected")
            
        num_players = len(villain_ranges) + 1
        
        # Initialize results
        wins = [0.0] * num_players
        
        # Run simulations
        for _ in range(num_simulations):
            # Setup and deal all cards
            villain_cards, final_board, _ = self.board_setup.setup_and_deal(
                hero_cards, board, len(villain_ranges)
            )
            
            # Evaluate hands and update win counts
            pot_shares = self._evaluate_hands_and_winners(
                hero_cards, villain_cards, final_board
            )
            for player, share in pot_shares.items():
                wins[player] += share
        
        # Calculate final equities
        return [win / num_simulations * 100 for win in wins]

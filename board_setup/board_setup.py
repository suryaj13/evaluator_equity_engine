import random
from typing import List, Optional, Tuple
from evaluator.hand import Card

class BoardSetup:
    def __init__(self):
        """
        Initialize the board setup.
        Creates a fresh deck of 52 cards using standard poker ranks and suits.
        """
        self.deck = [Card(r, s) for r in '23456789TJQKA' for s in 'shdc']

    def _handle_cards(self, 
                     cards_to_remove: List[Card], 
                     num_to_deal: Optional[int] = None) -> List[Card]:
        """
        Handle card operations: removing cards and optionally dealing new ones.
        
        Args:
            cards_to_remove: Cards to remove from the deck
            num_to_deal: Optional number of cards to deal from remaining deck
            
        Returns:
            If num_to_deal is specified, returns dealt cards
            Otherwise, returns remaining deck after removal
        """
        # Create set of removed card strings for efficient lookup
        removed_cards = {(c.rank + c.suit) for c in cards_to_remove}
        
        # Filter available cards
        available_cards = [
            card for card in self.deck 
            if (card.rank + card.suit) not in removed_cards
        ]
        
        if num_to_deal is not None:
            if num_to_deal > len(available_cards):
                raise ValueError("Not enough cards remaining to deal")
            return random.sample(available_cards, num_to_deal)
        return available_cards

    def setup_and_deal(self,
                      hero_cards: List[Card],
                      board: List[Card],
                      num_villains: int) -> Tuple[List[Card], List[Card], List[Card]]:
        """
        Setup simulation and deal all necessary cards.
        
        Args:
            hero_cards: Hero's hole cards
            board: Current board cards
            num_villains: Number of villains
            
        Returns:
            Tuple of (villain_cards, final_board, remaining_cards)
        """
        # Get available cards after removing known cards
        available_cards = self._handle_cards(hero_cards + board)
        
        # Deal villain cards
        villain_cards = []
        for _ in range(num_villains):
            villain_hand = self._handle_cards(hero_cards + board + villain_cards, 2)
            villain_cards.extend(villain_hand)
        
        # Complete board if needed
        remaining_cards = [c for c in available_cards if c not in villain_cards]
        remaining_board = 5 - len(board)
        final_board = (board + self._handle_cards(hero_cards + board + villain_cards, 
                                                remaining_board)) if remaining_board > 0 else board
        
        return villain_cards, final_board, remaining_cards 
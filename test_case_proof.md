```text
Player 1 hole: Jd 5d
Player 2 hole: Kd 4c
Player 3 hole: 7h 3d

Pairwise comparisons:
Player 1 (High Card: Jd 5d 2h Tc 4s) vs Player 2 (One Pair: Kd 4c 2h Tc 4s): Player 2 wins
Player 1 (High Card: Jd 5d 2h Tc 4s) vs Player 3 (High Card: 7h 3d 2h Tc 4s): Player 1 wins
Player 2 (One Pair: Kd 4c 2h Tc 4s) vs Player 3 (High Card: 7h 3d 2h Tc 4s): Player 2 wins

Winner: Player 2 with hand: One Pair: Kd 4c 2h Tc 4s

Edge case: identical hands should tie
Edge case passed: tie confirmed

✅ all randomized tests passed
suryaj@oakes-100-64-93-174 evaluator_equity_engine % python tests/test_evaluator.py

3-player showdown test...
Board: Kc Td Tc Jc 9h
Player 1 hole: Qs 8s
Player 2 hole: 9c 6c
Player 3 hole: Ts 9s

Pairwise comparisons:
Player 1 (Straight: Qs 8s Kc Td Tc) vs Player 2 (Flush: 9c 6c Kc Td Tc): Player 2 wins
Player 1 (Straight: Qs 8s Kc Td Tc) vs Player 3 (Full House: Ts 9s Kc Td Tc): Player 3 wins
Player 2 (Flush: 9c 6c Kc Td Tc) vs Player 3 (Full House: Ts 9s Kc Td Tc): Player 3 wins

Winner: Player 3 with hand: Full House: Ts 9s Kc Td Tc

Edge case: identical hands should tie
Edge case passed: tie confirmed


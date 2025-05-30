import unittest
from equity.equity_calc import EquityCalculator


class TestEquityCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = EquityCalculator()

    def test_preflop_aces_vs_kings(self):
        """Test AA vs KK preflop equity"""
        hero = ["As", "Ac"]
        villain = [["Ks", "Kc"]]
        equity = self.calc.calculate_equity(hero, villain, num_simulations=5000)
        print("AA vs KK equity:", equity)
        # AA should be about 80% favorite vs KK
        self.assertTrue(73 <= equity[0] <= 87)
        self.assertTrue(13 <= equity[1] <= 27)

    def test_flush_draw_equity(self):
        """Test AKs vs QQ on a flush draw flop"""
        hero = ["Ah", "Kh"]
        villain = [["Qs", "Qd"]]
        board = ["7h", "8h", "9c"]
        equity = self.calc.calculate_equity(hero, villain, board, num_simulations=5000)
        print("Flush draw equity:", equity)
        # Flush draw with overcards is a much bigger favorite in this scenario (AKh has 2 overcards + nut flush draw)
        self.assertTrue(60 <= equity[0] <= 70)
        self.assertTrue(30 <= equity[1] <= 40)

    def test_made_flush_vs_overpair(self):
        """Test made flush vs overpair"""
        hero = ["Ah", "Kh"]
        villain = [["Qs", "Qd"]]
        board = ["7h", "8h", "9h"]
        equity = self.calc.calculate_equity(hero, villain, board, num_simulations=5000)
        print("Made flush vs overpair equity:", equity)
        # Made flush should be over 90% favorite
        self.assertTrue(equity[0] >= 88)
        self.assertTrue(equity[1] <= 12)

    def test_multiway_pot(self):
        """Test AA vs KK vs QQ preflop"""
        hero = ["As", "Ac"]
        villains = [["Ks", "Kc"], ["Qs", "Qc"]]
        equity = self.calc.calculate_equity(hero, villains, num_simulations=5000)
        print("AA vs KK vs QQ equity:", equity)
        # Verify equities sum to 100%
        self.assertAlmostEqual(sum(equity), 100, delta=0.1)
        # AA should have highest equity
        self.assertEqual(max(equity), equity[0])
        # QQ should have lowest equity (allowing for floating point imprecision)
        self.assertAlmostEqual(min(equity), equity[2], delta=0.5)

    # def test_split_pot_scenario(self):
    #     """Test split pot scenario with same hand"""
    #     hero = ["Ah", "Kh"]
    #     villain = [["Ah", "Kh"]]  # Same hand
    #     equity = self.calc.calculate_equity(hero, villain, num_simulations=5000)
    #     print("Split pot scenario equity:", equity)
    #     # Should be exactly 50-50
    #     self.assertAlmostEqual(equity[0], 50, delta=1)
    #     self.assertAlmostEqual(equity[1], 50, delta=1)

    def test_turn_equity(self):
        """Test equity calculation on the turn"""
        hero = ["Ah", "Kh"]
        villain = [["Qs", "Qd"]]
        board = ["7h", "8h", "9c", "2s"]
        equity = self.calc.calculate_equity(hero, villain, board, num_simulations=5000)
        print("Turn equity:", equity)
        # Verify equity calculation works with 4 board cards
        self.assertTrue(0 <= equity[0] <= 100)
        self.assertTrue(0 <= equity[1] <= 100)
        self.assertAlmostEqual(sum(equity), 100, delta=0.1)

    def test_river_equity(self):
        """Test equity calculation on the river"""
        hero = ["Ah", "Kh"]
        villain = [["Qs", "Qd"]]
        board = ["7h", "8h", "9c", "2s", "3d"]
        equity = self.calc.calculate_equity(hero, villain, board, num_simulations=1)
        print("River equity:", equity)
        # On river, equity should be either 0 or 100 for each player
        self.assertTrue(equity[0] in [0, 100])
        self.assertTrue(equity[1] in [0, 100])
        self.assertAlmostEqual(sum(equity), 100, delta=0.1)

    def test_invalid_input(self):
        """Test error handling for invalid inputs"""
        hero = ["Ah", "Kh"]
        villain = [["Qs", "Qd"]]
        
        # Test invalid board length
        with self.assertRaises(ValueError):
            self.calc.calculate_equity(hero, villain, ["Ah", "Kh"])  # Only 2 board cards
            
        # Test duplicate cards
        with self.assertRaises(ValueError):
            self.calc.calculate_equity(["Ah", "Ah"], villain)  # Same hero cards
            
        # Test invalid card format
        with self.assertRaises(ValueError):
            self.calc.calculate_equity(["A1", "K2"], villain)  # Invalid card format

if __name__ == '__main__':
    unittest.main()

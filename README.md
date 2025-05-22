# ♠️ Poker Hand Equity & Evaluation Engine

A Python-based poker engine that evaluates hand strength and calculates equity through Monte Carlo simulations. Designed for scalability, testing, and integration into poker tools or bots.

## 🎯 Features
- Evaluate 5-card and 7-card poker hands
- Classify hands (Straight, Flush, Full House, etc.)
- Run equity simulations against 1+ random opponents
- Simulate unknown board cards
- Return win/tie/loss probabilities with customizable runs

## 🧠 Technologies
- Python 3.10+
- NumPy (for performance)
- Pytest (for testing)
- CLI or Web UI integration ready

## 📁 Project Structure

```text
poker-equity-engine/
├── evaluator/  # Hand parsing and evaluation
│   ├── hand.py
│   └── evaluator.py
├── equity/  # Hand equity simulation logic
│   ├── simulator.py
│   └── equity_calc.py
├── tests/
│   ├── test_evaluator.py
│   └── test_equity.py
├── examples/
│   └── run_simulation.py
└── README.md

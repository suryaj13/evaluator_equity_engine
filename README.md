# ♠️ Texas Hold'em Hand Evaluator & Equity Engine

This project is a Python-based poker engine designed for evaluating and comparing 7-card Texas Hold'em hands. It also includes a Monte Carlo equity simulator to calculate win/tie/loss probabilities given any number of players and a board.

## 🧠 What It Does

- Computes the best 5-card hand from 7 cards (2 hole cards + 5 community cards)
- Classifies hand types: Straight, Flush, Full House, etc.
- Compares two or more players to determine the winner(s)
- Runs thousands of simulations to calculate equity for each hand

## 🎮 Why Use This?

This tool is ideal for:
- Learning how poker hand evaluation works under the hood
- Building poker bots or analysis tools
- Running custom equity calculations for specific game states
- Practicing algorithm design and simulation in Python

## ⚙️ Technologies

- Python 3
- `itertools` for combinatorics
- `collections.Counter` for frequency analysis
- (Planned) NumPy for faster simulation
- `pytest` for unit testing

## 📁 Project Structure

```text
poker-equity-engine/
├── evaluator/           # All logic for parsing and evaluating hands
│   ├── hand.py
│   ├── evaluator.py
│   └── __init__.py
├── equity/              # Simulation & probability logic
│   ├── equity_calc.py
│   └── simulator.py
├── tests/               # Test suite
│   ├── test_evaluator.py
│   └── test_equity.py
├── main.py              # Optional CLI entry point
├── README.md</file>
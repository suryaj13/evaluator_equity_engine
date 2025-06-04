# Texas Hold'em Hand Evaluator & Equity Engine

This project is a Python-based poker engine designed for evaluating and comparing 7-card Texas Hold'em hands. It also includes a Monte Carlo equity simulator to calculate win/tie/loss probabilities given any number of players and a board.

## What It Does

- Computes the best 5-card hand from 7 cards (2 hole cards + 5 community cards)
- Classifies hand types: Straight, Flush, Full House, etc.
- Compares two or more players to determine the winner(s)
- Runs thousands of simulations to calculate equity for each hand
- Modular design: separates board/card setup logic from equity simulation logic

##  Why Use This?

This tool is ideal for:
- Learning how poker hand evaluation works under the hood
- Building poker bots or analysis tools
- Running custom equity calculations for specific game states
- Practicing algorithm design and simulation in Python

## Technologies

- Python 3
- `itertools` for combinatorics
- `collections.Counter` for frequency analysis
- (Planned) NumPy for faster simulation
- `pytest` and `unittest` for unit testing

##  Project Structure

```text
poker-equity-engine/
├── evaluator/           # All logic for parsing and evaluating hands
│   ├── hand.py
│   ├── evaluator.py
│   └── __init__.py
├── equity/              # Simulation & probability logic
│   ├── equity_calc.py   # Monte Carlo equity engine (uses BoardSetup)
│   └── simulator.py
├── board_setup/         # Board and card dealing logic
│   └── board_setup.py
├── tests/               # Test suite (unittest-based)
│   ├── test_evaluator.py
│   └── test_equity.py
├── examples/            # Example scripts (optional)
├── main.py              # Optional CLI entry point
├── README.md
```

## Running Tests

From the project root, run:

```sh
python -m unittest discover tests
```

Or, to run a specific test file:

```sh
python -m tests.test_equity
```

## Notes on Equity Results

- The equity engine uses Monte Carlo simulation, so results may vary slightly between runs.
- The flush draw test (AKh vs QQ on 7h 8h 9c) expects AKh to have 60–70% equity, reflecting the nut flush draw plus two overcards.
- For more stable results, tests use 5000+ simulations per scenario.
- Split-pot scenarios with duplicate hands are not supported by default (to match real poker rules).

## Extending
- To add new evaluation logic, update `evaluator/evaluator.py` and `evaluator/hand.py`.
- To add new simulation or board logic, update `equity/equity_calc.py` or `board_setup/board_setup.py`.
- To add new tests, place them in the `tests/` directory.

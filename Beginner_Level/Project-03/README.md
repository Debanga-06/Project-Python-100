# Number Guessing Game (Python CLI) ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow) [![License](https://img.shields.io/github/license/Debanga-06/Code-Odessey)](https://github.com/Debanga-06/Code-Odessey/blob/main/LICENSE)


A clean, beginner-friendly command-line game where the computer picks a secret number and you guess until you’re right. Get instant higher/lower hints, an attempt counter, and configurable ranges/difficulty.


---

## ✨ Features

 - True CLI app using only Python standard library

 - Configurable range (--min, --max)

 - Optional strict mode (counts invalid inputs as attempts)

 - Deterministic runs for testing (--seed)

 - Clear separation of game logic and I/O



---

## 🚀 Quick Start

- Requires Python 3.8+

- python3 game.py

You’ll see a prompt like:

    🎯 I picked a number between 1 and 100. Can you guess it?
    Your guess:


---

## 🔧 Installation

No external dependencies.
```

git clone https://github.com/Debanga-06/B2A-Python
cd number-guessing-game
python3 game.py

```


---

## ▶️ Usage

     python3 game.py 
       [--min MIN]
       [--max MAX] 
       [--hard] 
       [--seed SEED]

Options

- --min <int>: Lower bound (default: 1)

- --max <int>: Upper bound (default: 100)

- --hard: Count invalid/out-of-range inputs as attempts

- --seed <int>: Deterministic secret for testing


## Examples

- Classic 1–100

      python3 game.py

- Custom range 1–1000

      python3 game.py --min 1 --max 1000

- Strict mode (invalid inputs count)

      python3 game.py --hard

- Reproducible secret (great for tests/CI)

      python3 game.py --seed 42


---

## 🗂️ Project Structure

number-guessing-game/

    ├─ README.md
    ├─ LICENSE 
    ├─ game.py               # CLI entrypoint
    └─ tests/
         └─ test_core.py     # unit tests

> Keep business logic in src/core.py if you plan to test or extend the game.




---

## 🧠 How It Works (Pseudocode)

```
parse CLI args (min, max, hard, seed)
rng = Random(seed)
secret = rng.randint(min, max)
attempts = 0

loop:
  read input
  if invalid or out of range:
    if hard: attempts += 1
    prompt again
  else:
    attempts += 1
    compare guess vs secret
    print "Too low" / "Too high" or success with attempts

```
---

## 🧪 Testing

Example pytest (optional):

```
 tests/test_core.py

from random import Random

def choose_secret(rng, lo, hi):
    return rng.randint(lo, hi)

def test_secret_in_range():
    rng = Random(123)
    lo, hi = 1, 100
    s = choose_secret(rng, lo, hi)
    assert lo <= s <= hi

Run tests:

pytest -q

```
---

## 🔒 Input Validation

- Non-integer inputs prompt a retry (and count as attempts in --hard mode).

- Out-of-range inputs prompt guidance (and may count in --hard mode).

- --min must be strictly less than --max; 

    else the program exits with an error.



---

## ♿ Accessibility & UX Notes

- Uses plain text prompts suitable for screen readers/terminal UIs.

- Avoids color-only feedback; messages are descriptive (“Too low/Too high/Correct!”).



---

## 🛣️ Roadmap (Nice-to-Have)

- “Temperature” hints (e.g., “Very close!”)

- Timed mode + local high-score file

- JSON config file & env var support

- GUI (Tkinter) or web (Flask/FastAPI) front-end

- Localization (gettext)



---

## 🤝 Contributing

1. Fork the repo


2. Create a feature branch: git checkout -b feat/better-hints


3. Commit: git commit -m "Add temperature-style hints"


4. Push & open a PR



Please include tests for new logic and keep I/O clean.


---

## 📜 License

-  This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

## 🔗 References (Official Docs)

- Python random (PRNG, randint): https://docs.python.org/3/library/random.html

- Python argparse (CLI flags): https://docs.python.org/3/library/argparse.html

- Built-in input() / print() behavior: https://docs.python.org/3/library/functions.html#input

- unittest (if you use stdlib tests): https://docs.python.org/3/library/unittest.html

- pytest (popular test runner): https://docs.pytest.org/


These are reputable, official sources for the Python features used in this project.
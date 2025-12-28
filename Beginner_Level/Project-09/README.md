# Dice Rolling Simulator 

A Python program that simulates rolling dice with beautiful ASCII art visualization.

## Features

- Roll 1 to 5 dice at once
- Beautiful ASCII art dice display with Unicode characters
- Shows individual dice results
- Calculates and displays total sum automatically
- Interactive rolling experience
- Unlimited rolls per session
- Input validation and error handling

## Requirements

- Python 3.x
- Terminal with Unicode support (for dice symbols ●)

## How to Run

1. Save the program as `dice_simulator.py`
2. Open your terminal or command prompt
3. Navigate to the directory containing the file
4. Run the program:

```bash
python dice_simulator.py
```

## Usage Example

```
==================================================
        DICE ROLLING SIMULATOR
==================================================

--------------------------------------------------
How many dice to roll? (1-5, default 1): 2

Press Enter to roll the dice...

🎲 Rolling the dice... 🎲

┌─────────┐  ┌─────────┐
│  ●   ●  │  │  ●      │
│    ●    │  │    ●    │
│  ●   ●  │  │      ●  │
└─────────┘  └─────────┘

Results: [5, 3]
Total: 8

Roll again? (Y/n): n

Thanks for playing!
```

## Dice Values Explained

Each die shows a value from 1 to 6 using dots (●):

| Value | Description | Pattern |
|-------|-------------|---------|
| **1** | Single dot in center | Center only |
| **2** | Two dots diagonally | Top-left, bottom-right |
| **3** | Three dots diagonally | Top-left, center, bottom-right |
| **4** | Four dots in corners | All four corners |
| **5** | Five dots | Four corners + center |
| **6** | Six dots | Two columns of three |

## How It Works

1. **User Input**: Choose number of dice (1-5)
2. **Random Generation**: Uses Python's `random.randint(1, 6)` for fair rolls
3. **ASCII Art Display**: Each value mapped to Unicode box art
4. **Results**: Shows individual values and sum

## Use Cases

- Board games (Monopoly, Backgammon, Yahtzee, etc.)
- Role-playing games (D&D using d6)
- Teaching probability and statistics
- Random number generation for games
- Decision making tool
- Programming demonstration of ASCII art

## Probability

Each die has equal probability for each value:
- Probability of any single value: 1/6 (≈16.67%)
- For two dice, possible totals range from 2 to 12
- Most common total with two dice: 7

## Code Structure

- `roll_dice(num_dice)` - Generates random dice values using list comprehension
- `display_dice(value)` - Returns ASCII art list for a given dice value
- `main()` - Handles user interaction, input validation, and display formatting

## Technical Details

- Uses Python's `random` module for secure randomization
- Each die roll is independent and fair (1/6 probability)
- Unicode box-drawing characters create clean dice visuals
- Multiple dice displayed side-by-side using string joining

## Customization Ideas

- Add support for different dice types (d4, d8, d10, d12, d20)
- Track roll history and statistics
- Add dice rolling animations
- Support for weighted or loaded dice
- Multiplayer mode with separate rolls

## License

Free to use and modify for any purpose.
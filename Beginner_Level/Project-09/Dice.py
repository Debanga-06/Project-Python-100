import random


def roll_dice(num_dice=1):
    """
    Roll one or more dice and return the results.
    """
    return [random.randint(1, 6) for _ in range(num_dice)]


def display_dice(value):
    """
    Display dice using ASCII art.
    """
    dice_art = {
        1: [
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"
        ],
        2: [
            "┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘"
        ],
        3: [
            "┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘"
        ],
        4: [
            "┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        5: [
            "┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        6: [
            "┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘"
        ]
    }
    return dice_art[value]


def main():
    print("=" * 50)
    print("        DICE ROLLING SIMULATOR")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 50)
        
        try:
            num_dice = input("How many dice to roll? (1-5, default 1): ").strip()
            num_dice = int(num_dice) if num_dice else 1
            
            if num_dice < 1 or num_dice > 5:
                print("Please choose between 1 and 5 dice.")
                continue
            
            input("\nPress Enter to roll the dice...")
            
            results = roll_dice(num_dice)
            
            print("\n🎲 Rolling the dice... 🎲\n")
            
            # Display all dice side by side
            if num_dice == 1:
                for line in display_dice(results[0]):
                    print(line)
            else:
                # Print dice horizontally
                dice_lines = [display_dice(val) for val in results]
                for i in range(5):  # 5 lines per dice
                    line = "  ".join(dice[i] for dice in dice_lines)
                    print(line)
            
            print(f"\nResults: {results}")
            print(f"Total: {sum(results)}")
            
        except ValueError:
            print("Invalid input.")
            continue
        
        again = input("\nRoll again? (Y/n): ")
        if again.lower() == 'n':
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
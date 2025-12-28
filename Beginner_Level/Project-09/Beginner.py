import random

def roll_dice():
    return random.randint(1, 6)

if __name__ == "__main__":
    print("Rolling the dice...")
    result = roll_dice()
    print(f"You rolled a {result}!")

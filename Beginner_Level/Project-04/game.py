import random

CHOICES = ("rock", "paper", "scissors")

# Rules: what each move defeats
WINS_AGAINST = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}

def determine_winner(player, computer):
    if player == computer:
        return "draw"
    return "player" if WINS_AGAINST[player] == computer else "computer"

def get_player_choice():
    while True:
        choice = input("Choose rock, paper, or scissors (or 'q' to quit): ").strip().lower()
        if choice in ("q", "quit", "exit"):
            return None
        if choice in CHOICES:
            return choice
        print("Invalid choice. Please type rock, paper, or scissors.")

def play_round():
    player = get_player_choice()
    if player is None:
        return None  # signal to stop
    computer = random.choice(CHOICES)
    result = determine_winner(player, computer)

    print(f"\nYou chose: {player}")
    print(f"Computer chose: {computer}")

    if result == "draw":
        print("Result: It's a draw!\n")
    elif result == "player":
        print("Result: You win! 🎉\n")
    else:
        print("Result: Computer wins! 🤖\n")

    return result

def main():
    print("=== Rock · Paper · Scissors ===")
    player_score = 0
    computer_score = 0
    rounds_played = 0

    while True:
        outcome = play_round()
        if outcome is None:
            break
        rounds_played += 1
        if outcome == "player":
            player_score += 1
        elif outcome == "computer":
            computer_score += 1

        print(f"Score — You: {player_score} | Computer: {computer_score} | Rounds: {rounds_played}\n")

    print("\nThanks for playing!")
    print(f"Final Score — You: {player_score} | Computer: {computer_score} | Rounds: {rounds_played}")
    print("Come Again,and beat computer .")

if __name__ == "__main__":
    main()
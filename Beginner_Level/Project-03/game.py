import random

LOW, HIGH = 1, 100
secret = random.randint(LOW, HIGH)
attempts = 0

print(f"I'm thinking of a number between {LOW} and {HIGH}. Can you guess it?")

while True:
    guess_str = input("Your guess: ").strip()
    if not guess_str.isdigit():
        print("Please enter a valid positive integer.")
        continue

    guess = int(guess_str)
    attempts += 1

    if guess < secret:
        print("Too low! Try again.")
    elif guess > secret:
        print("Too high! Try again.")
    else:
        print(f"🎉 Correct! The number was {secret}. You got it in {attempts} tries.")
        break
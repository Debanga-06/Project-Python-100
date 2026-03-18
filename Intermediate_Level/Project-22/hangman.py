import tkinter as tk
from tkinter import messagebox
import random
import os

# File I/O: Load words
words_file = "words.txt"
if not os.path.exists(words_file):
    with open(words_file, "w") as f:
        f.write("python\nprogramming\nhangman\ndeveloper\nkeyboard\ncomputer\nalgorithm\nfunction\nvariable\n")

with open(words_file, "r") as f:
    word_list = [line.strip().lower() for line in f if line.strip()]

# Game Logic
class HangmanGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.word = random.choice(word_list)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong = 6

    def guess(self, letter):
        letter = letter.lower()
        if letter in self.guessed_letters:
            return "already"
        self.guessed_letters.append(letter)
        if letter not in self.word:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong:
                return "lose"
        else:
            if all(l in self.guessed_letters for l in self.word):
                return "win"
        return "continue"

    def display_word(self):
        return " ".join([l if l in self.guessed_letters else "_" for l in self.word])

    def remaining_attempts(self):
        return self.max_wrong - self.wrong_guesses

# GUI
game = HangmanGame()
root = tk.Tk()
root.title("Hangman Game")
root.geometry("500x400")

word_label = tk.Label(root, text=game.display_word(), font=("Helvetica", 24))
word_label.pack(pady=20)

info_label = tk.Label(root, text=f"Remaining attempts: {game.remaining_attempts()}", font=("Helvetica", 14))
info_label.pack(pady=10)

entry = tk.Entry(root, font=("Helvetica", 18), width=5)
entry.pack(pady=10)
entry.focus()  # Start with cursor in entry

def submit_guess(event=None):
    letter = entry.get().strip()
    entry.delete(0, tk.END)
    if len(letter) != 1 or not letter.isalpha():
        messagebox.showwarning("Invalid input", "Please enter a single alphabet letter.")
        return
    result = game.guess(letter)
    word_label.config(text=game.display_word())
    info_label.config(text=f"Remaining attempts: {game.remaining_attempts()}")
    
    if result == "win":
        messagebox.showinfo("Hangman", f"Congratulations! You guessed the word: {game.word}")
        game.reset_game()
        word_label.config(text=game.display_word())
        info_label.config(text=f"Remaining attempts: {game.remaining_attempts()}")
    elif result == "lose":
        messagebox.showinfo("Hangman", f"Game Over! The word was: {game.word}")
        game.reset_game()
        word_label.config(text=game.display_word())
        info_label.config(text=f"Remaining attempts: {game.remaining_attempts()}")
    elif result == "already":
        messagebox.showwarning("Hangman", f"You already guessed '{letter}'.")

# Bind Enter key to submit_guess
entry.bind("<Return>", submit_guess)

# Guess Button
submit_btn = tk.Button(root, text="Guess", command=submit_guess)
submit_btn.pack(pady=10)

root.mainloop()
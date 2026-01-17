# Flashcards App (CLI) (Beginner Level)

import random

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class FlashcardApp:
    def __init__(self):
        self.flashcards = []

    def load_flashcards(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                question, answer = line.strip().split(',')
                self.flashcards.append(Flashcard(question, answer))

    def add_flashcard(self, question, answer):
        self.flashcards.append(Flashcard(question, answer))

    def practice(self):
        random.shuffle(self.flashcards)
        for flashcard in self.flashcards:
            user_answer = input(f"Q: {flashcard.question} ")
            if user_answer.lower() == flashcard.answer.lower():
                print("Correct!")
            else:
                print(f"Wrong! The correct answer is: {flashcard.answer}")

if __name__ == "__main__":
    app = FlashcardApp()
    app.load_flashcards('flashcards.txt')
    app.practice()

# Flashcards App

A simple Python-based flashcards application for creating, managing, and quizzing yourself on question-answer pairs. Flashcards are stored in a JSON file (`flashcards.json`) for persistence.

## Features

- **Add Flashcard**: Create a new flashcard with a question and answer.
- **View Flashcards**: Display all saved flashcards.
- **Update Flashcard**: Modify an existing flashcard's answer.
- **Delete Flashcard**: Remove a flashcard by question.
- **Quiz Mode**: Test yourself with all flashcards and get a score.
- **Validation**: Ensures questions and answers are not empty.

## Requirements

- Python 3.x

## How to Run

1. Run the `Flashcards.py` script:
   ```
   python Flashcards.py
   ```
2. Follow the menu prompts to perform operations.

## Usage

- Choose an option from the menu (1-6).
- For adding/updating, enter non-empty questions and answers.
- In quiz mode, answers are case-insensitive.
- Flashcards are automatically saved to `flashcards.json`.

## Example

```
Enter choice: 1
Enter Question: What is the capital of France?
Enter Answer: Paris
✅ Flashcard added successfully!

Enter choice: 5
--- Quiz Mode ---
Q: What is the capital of France?
Your Answer: paris
✅ Correct!

📊 Your Score: 1/1
```

## Notes

- Data is stored in JSON format; not encrypted.
- Quiz mode compares answers case-insensitively after stripping whitespace.
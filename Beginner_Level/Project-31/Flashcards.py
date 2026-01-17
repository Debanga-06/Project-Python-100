import json
import os

FLASHCARDS_FILE = "flashcards.json"

# ---------- Helper Functions ----------
def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_flashcards(flashcards):
    with open(FLASHCARDS_FILE, "w") as f:
        json.dump(flashcards, f, indent=4)

# ---------- Validation ----------
def validate_input(text, field_name):
    if not text.strip():
        print(f"⚠️ {field_name} cannot be empty!")
        return False
    return True

# ---------- CRUD Operations ----------
def add_flashcard(flashcards):
    question = input("Enter Question: ")
    if not validate_input(question, "Question"):
        return
    answer = input("Enter Answer: ")
    if not validate_input(answer, "Answer"):
        return

    flashcards[question] = answer
    save_flashcards(flashcards)
    print("✅ Flashcard added successfully!")

def view_flashcards(flashcards):
    if not flashcards:
        print("No flashcards found.")
    else:
        print("\n--- Flashcards ---")
        for q, a in flashcards.items():
            print(f"Q: {q}\nA: {a}\n")

def update_flashcard(flashcards):
    question = input("Enter the question to update: ")
    if question in flashcards:
        new_answer = input("Enter new Answer: ")
        if not validate_input(new_answer, "Answer"):
            return
        flashcards[question] = new_answer
        save_flashcards(flashcards)
        print("✅ Flashcard updated successfully!")
    else:
        print("⚠️ Flashcard not found.")

def delete_flashcard(flashcards):
    question = input("Enter the question to delete: ")
    if question in flashcards:
        del flashcards[question]
        save_flashcards(flashcards)
        print("✅ Flashcard deleted successfully!")
    else:
        print("⚠️ Flashcard not found.")

def quiz(flashcards):
    if not flashcards:
        print("No flashcards available for quiz.")
        return
    print("\n--- Quiz Mode ---")
    score = 0
    total = len(flashcards)
    for q, a in flashcards.items():
        print(f"Q: {q}")
        user_answer = input("Your Answer: ")
        if user_answer.strip().lower() == a.strip().lower():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! Correct Answer: {a}\n")
    print(f"📊 Your Score: {score}/{total}")

# ---------- Main Program ----------
def main():
    flashcards = load_flashcards()
    while True:
        print("\n--- Flashcards Menu ---")
        print("1. Add Flashcard")
        print("2. View Flashcards")
        print("3. Update Flashcard")
        print("4. Delete Flashcard")
        print("5. Quiz Yourself")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_flashcard(flashcards)
        elif choice == "2":
            view_flashcards(flashcards)
        elif choice == "3":
            update_flashcard(flashcards)
        elif choice == "4":
            delete_flashcard(flashcards)
        elif choice == "5":
            quiz(flashcards)
        elif choice == "6":
            print("Exiting Flashcards App. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
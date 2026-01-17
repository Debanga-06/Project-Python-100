# Advanced Level

import json
import os
import random
from datetime import datetime


class Flashcard:
    """Represents a single flashcard."""
    
    def __init__(self, question, answer, deck_name="General", card_id=None):
        """Initialize a flashcard."""
        self.id = card_id if card_id else self._generate_id()
        self.question = question
        self.answer = answer
        self.deck_name = deck_name
        self.times_studied = 0
        self.times_correct = 0
        self.times_incorrect = 0
        self.last_studied = None
        self.created_at = datetime.now().isoformat()
    
    def _generate_id(self):
        """Generate unique ID for card."""
        return f"card_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def study(self, correct):
        """Record study session result."""
        self.times_studied += 1
        if correct:
            self.times_correct += 1
        else:
            self.times_incorrect += 1
        self.last_studied = datetime.now().isoformat()
    
    def get_accuracy(self):
        """Calculate accuracy percentage."""
        if self.times_studied == 0:
            return 0.0
        return (self.times_correct / self.times_studied) * 100
    
    def to_dict(self):
        """Convert to dictionary for JSON storage."""
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "deck_name": self.deck_name,
            "times_studied": self.times_studied,
            "times_correct": self.times_correct,
            "times_incorrect": self.times_incorrect,
            "last_studied": self.last_studied,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create flashcard from dictionary."""
        card = cls(data["question"], data["answer"], data["deck_name"], data["id"])
        card.times_studied = data.get("times_studied", 0)
        card.times_correct = data.get("times_correct", 0)
        card.times_incorrect = data.get("times_incorrect", 0)
        card.last_studied = data.get("last_studied")
        card.created_at = data.get("created_at", datetime.now().isoformat())
        return card


class FlashcardDeck:
    """Manages a collection of flashcards."""
    
    def __init__(self, filename="flashcards.json"):
        """Initialize deck with file storage."""
        self.filename = filename
        self.cards = []
        self.load_cards()
    
    def load_cards(self):
        """Load cards from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.cards = [Flashcard.from_dict(card_data) for card_data in data]
            except Exception as e:
                print(f"⚠️  Error loading cards: {e}")
                self.cards = []
        else:
            self.cards = []
    
    def save_cards(self):
        """Save cards to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump([card.to_dict() for card in self.cards], f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving cards: {e}")
            return False
    
    def add_card(self, question, answer, deck_name="General"):
        """Add new flashcard."""
        card = Flashcard(question, answer, deck_name)
        self.cards.append(card)
        self.save_cards()
        return card
    
    def remove_card(self, card_id):
        """Remove flashcard by ID."""
        self.cards = [card for card in self.cards if card.id != card_id]
        self.save_cards()
    
    def get_card_by_id(self, card_id):
        """Get card by ID."""
        for card in self.cards:
            if card.id == card_id:
                return card
        return None
    
    def get_cards_by_deck(self, deck_name):
        """Get all cards in a specific deck."""
        return [card for card in self.cards if card.deck_name == deck_name]
    
    def get_all_deck_names(self):
        """Get list of unique deck names."""
        return list(set(card.deck_name for card in self.cards))
    
    def get_cards_needing_review(self):
        """Get cards that need more practice (low accuracy)."""
        return [card for card in self.cards 
                if card.times_studied > 0 and card.get_accuracy() < 75]
    
    def search_cards(self, keyword):
        """Search cards by keyword in question or answer."""
        keyword = keyword.lower()
        return [card for card in self.cards 
                if keyword in card.question.lower() or keyword in card.answer.lower()]


def display_card_details(card):
    """Display detailed information about a card."""
    print("\n" + "=" * 70)
    print(f"Card ID: {card.id}")
    print("=" * 70)
    print(f"Deck:        {card.deck_name}")
    print(f"\nQuestion:    {card.question}")
    print(f"Answer:      {card.answer}")
    print(f"\nStatistics:")
    print(f"  Times Studied:    {card.times_studied}")
    print(f"  Correct:          {card.times_correct}")
    print(f"  Incorrect:        {card.times_incorrect}")
    print(f"  Accuracy:         {card.get_accuracy():.1f}%")
    if card.last_studied:
        print(f"  Last Studied:     {card.last_studied[:19]}")
    print("=" * 70)


def study_session(deck, cards_to_study, mode="normal"):
    """
    Conduct a study session.
    
    Args:
        deck: FlashcardDeck instance
        cards_to_study: List of cards to study
        mode: "normal", "reverse" (answer->question), or "random"
    """
    if not cards_to_study:
        print("\n📭 No cards to study!")
        return
    
    # Shuffle cards for randomization
    study_cards = cards_to_study.copy()
    random.shuffle(study_cards)
    
    print("\n" + "=" * 70)
    print(f"STUDY SESSION - {len(study_cards)} cards")
    print("=" * 70)
    print("\nInstructions:")
    print("  • Read each question carefully")
    print("  • Think of your answer")
    print("  • Press Enter to reveal the answer")
    print("  • Mark yourself as correct (c) or incorrect (i)")
    print("  • Type 'quit' to exit early")
    
    input("\nPress Enter to begin...")
    
    correct_count = 0
    incorrect_count = 0
    
    for i, card in enumerate(study_cards, 1):
        print("\n" + "-" * 70)
        print(f"Card {i}/{len(study_cards)}")
        print("-" * 70)
        
        # Determine question and answer based on mode
        if mode == "reverse":
            question = card.answer
            answer = card.question
            print(f"\n📝 Answer: {question}")
        else:
            question = card.question
            answer = card.answer
            print(f"\n❓ Question: {question}")
        
        # Wait for user to think
        user_input = input("\nPress Enter to reveal answer (or 'quit' to exit): ").strip().lower()
        
        if user_input == 'quit':
            print("\n⚠️  Study session ended early.")
            break
        
        # Show answer
        if mode == "reverse":
            print(f"\n✅ Correct Question: {answer}")
        else:
            print(f"\n✅ Correct Answer: {answer}")
        
        # Get self-assessment
        while True:
            result = input("\nDid you get it right? (c=correct, i=incorrect): ").strip().lower()
            if result in ['c', 'i']:
                break
            print("⚠️  Please enter 'c' for correct or 'i' for incorrect.")
        
        # Record result
        is_correct = (result == 'c')
        card.study(is_correct)
        
        if is_correct:
            correct_count += 1
            print("✓ Great job!")
        else:
            incorrect_count += 1
            print("✗ Keep practicing!")
    
    # Save progress
    deck.save_cards()
    
    # Display session summary
    total = correct_count + incorrect_count
    if total > 0:
        accuracy = (correct_count / total) * 100
        
        print("\n" + "=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        print(f"Cards Studied:   {total}")
        print(f"Correct:         {correct_count}")
        print(f"Incorrect:       {incorrect_count}")
        print(f"Accuracy:        {accuracy:.1f}%")
        
        # Performance feedback
        if accuracy >= 90:
            print("\n🌟 Excellent! You're mastering this material!")
        elif accuracy >= 75:
            print("\n⭐ Good work! You're getting there!")
        elif accuracy >= 60:
            print("\n✨ Keep practicing! You're improving!")
        else:
            print("\n📚 Review recommended. Practice makes perfect!")
        
        print("=" * 70)


def display_statistics(deck):
    """Display overall statistics."""
    if not deck.cards:
        print("\n📊 No cards to analyze yet.")
        return
    
    total_cards = len(deck.cards)
    studied_cards = len([c for c in deck.cards if c.times_studied > 0])
    unstudied_cards = total_cards - studied_cards
    
    total_studies = sum(c.times_studied for c in deck.cards)
    total_correct = sum(c.times_correct for c in deck.cards)
    total_incorrect = sum(c.times_incorrect for c in deck.cards)
    
    overall_accuracy = (total_correct / total_studies * 100) if total_studies > 0 else 0
    
    print("\n" + "=" * 70)
    print("OVERALL STATISTICS")
    print("=" * 70)
    
    print(f"\n📚 Card Collection:")
    print(f"   Total Cards:      {total_cards}")
    print(f"   Studied:          {studied_cards}")
    print(f"   Not Yet Studied:  {unstudied_cards}")
    print(f"   Decks:            {len(deck.get_all_deck_names())}")
    
    if total_studies > 0:
        print(f"\n📊 Study Statistics:")
        print(f"   Total Reviews:    {total_studies}")
        print(f"   Correct:          {total_correct}")
        print(f"   Incorrect:        {total_incorrect}")
        print(f"   Overall Accuracy: {overall_accuracy:.1f}%")
    
    # Cards needing review
    need_review = deck.get_cards_needing_review()
    if need_review:
        print(f"\n⚠️  Cards Needing Review: {len(need_review)}")
        print("   (Cards with <75% accuracy)")
    
    # Deck breakdown
    decks = deck.get_all_deck_names()
    if decks:
        print(f"\n📦 Decks:")
        for deck_name in sorted(decks):
            deck_cards = deck.get_cards_by_deck(deck_name)
            print(f"   {deck_name}: {len(deck_cards)} cards")
    
    print("=" * 70)


def list_cards(cards, title="Cards"):
    """Display a list of cards."""
    if not cards:
        print(f"\n📭 No {title.lower()} found.")
        return
    
    print("\n" + "=" * 70)
    print(f"{title.upper()} ({len(cards)})")
    print("=" * 70)
    
    for i, card in enumerate(cards, 1):
        accuracy = f"{card.get_accuracy():.0f}%" if card.times_studied > 0 else "Not studied"
        print(f"\n{i}. [{card.deck_name}]")
        print(f"   Q: {card.question[:50]}{'...' if len(card.question) > 50 else ''}")
        print(f"   A: {card.answer[:50]}{'...' if len(card.answer) > 50 else ''}")
        print(f"   Accuracy: {accuracy} | Studies: {card.times_studied}")
    
    print("=" * 70)


def main():
    """Main program execution."""
    deck = FlashcardDeck()
    
    print("=" * 70)
    print("                    FLASHCARDS APP (CLI)")
    print("=" * 70)
    print("\nStudy smarter with flashcards and spaced repetition!")
    
    while True:
        print("\n" + "-" * 70)
        print("Main Menu:")
        print("  1. Study all cards")
        print("  2. Study specific deck")
        print("  3. Study cards needing review")
        print("  4. Add new card")
        print("  5. View all cards")
        print("  6. Search cards")
        print("  7. Delete card")
        print("  8. View statistics")
        print("  9. Import sample cards")
        print("  q. Quit")
        print("-" * 70)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            if deck.save_cards():
                print("\n✓ Progress saved. Happy studying!")
            break
        
        try:
            if choice == '1':
                # Study all cards
                if not deck.cards:
                    print("\n📭 No cards available. Add some cards first!")
                    continue
                
                print("\nStudy Mode:")
                print("  1. Normal (Question → Answer)")
                print("  2. Reverse (Answer → Question)")
                print("  3. Random Mix")
                
                mode_choice = input("Select mode (1-3, default 1): ").strip()
                mode_map = {"1": "normal", "2": "reverse", "3": "random"}
                mode = mode_map.get(mode_choice, "normal")
                
                study_session(deck, deck.cards, mode)
            
            elif choice == '2':
                # Study specific deck
                deck_names = deck.get_all_deck_names()
                if not deck_names:
                    print("\n📭 No decks available.")
                    continue
                
                print("\nAvailable Decks:")
                for i, name in enumerate(sorted(deck_names), 1):
                    card_count = len(deck.get_cards_by_deck(name))
                    print(f"  {i}. {name} ({card_count} cards)")
                
                try:
                    deck_idx = int(input("\nSelect deck number: ")) - 1
                    selected_deck = sorted(deck_names)[deck_idx]
                    cards = deck.get_cards_by_deck(selected_deck)
                    
                    print("\nStudy Mode:")
                    print("  1. Normal (Question → Answer)")
                    print("  2. Reverse (Answer → Question)")
                    
                    mode_choice = input("Select mode (1-2, default 1): ").strip()
                    mode = "reverse" if mode_choice == "2" else "normal"
                    
                    study_session(deck, cards, mode)
                except (ValueError, IndexError):
                    print("❌ Invalid selection.")
            
            elif choice == '3':
                # Study cards needing review
                need_review = deck.get_cards_needing_review()
                if not need_review:
                    print("\n🎉 Great! All cards have good accuracy!")
                    continue
                
                print(f"\n📚 Found {len(need_review)} cards needing review")
                study_session(deck, need_review)
            
            elif choice == '4':
                # Add new card
                print("\n" + "=" * 70)
                print("ADD NEW FLASHCARD")
                print("=" * 70)
                
                question = input("\nQuestion: ").strip()
                if not question:
                    print("❌ Question cannot be empty.")
                    continue
                
                answer = input("Answer: ").strip()
                if not answer:
                    print("❌ Answer cannot be empty.")
                    continue
                
                # Show existing decks
                existing_decks = deck.get_all_deck_names()
                if existing_decks:
                    print("\nExisting decks:")
                    for i, name in enumerate(sorted(existing_decks), 1):
                        print(f"  {i}. {name}")
                
                deck_name = input("\nDeck name (default: General): ").strip()
                if not deck_name:
                    deck_name = "General"
                
                card = deck.add_card(question, answer, deck_name)
                print(f"\n✓ Card added to '{deck_name}' deck!")
            
            elif choice == '5':
                # View all cards
                if not deck.cards:
                    print("\n📭 No cards available.")
                    continue
                
                # Group by deck
                deck_names = deck.get_all_deck_names()
                for deck_name in sorted(deck_names):
                    cards = deck.get_cards_by_deck(deck_name)
                    list_cards(cards, f"{deck_name} Deck")
            
            elif choice == '6':
                # Search cards
                keyword = input("\nEnter search keyword: ").strip()
                if not keyword:
                    print("❌ Keyword cannot be empty.")
                    continue
                
                results = deck.search_cards(keyword)
                list_cards(results, f"Search Results for '{keyword}'")
            
            elif choice == '7':
                # Delete card
                if not deck.cards:
                    print("\n📭 No cards to delete.")
                    continue
                
                list_cards(deck.cards, "All Cards")
                
                try:
                    card_num = int(input("\nEnter card number to delete: ")) - 1
                    if 0 <= card_num < len(deck.cards):
                        card = deck.cards[card_num]
                        confirm = input(f"\nDelete: '{card.question}'? (y/n): ")
                        if confirm.lower() == 'y':
                            deck.remove_card(card.id)
                            print("✓ Card deleted.")
                    else:
                        print("❌ Invalid card number.")
                except ValueError:
                    print("❌ Invalid input.")
            
            elif choice == '8':
                # View statistics
                display_statistics(deck)
            
            elif choice == '9':
                # Import sample cards
                print("\n" + "=" * 70)
                print("IMPORT SAMPLE CARDS")
                print("=" * 70)
                print("\nImporting sample cards for:")
                print("  • Python Programming")
                print("  • General Knowledge")
                print("  • Math")
                
                confirm = input("\nImport samples? (y/n): ")
                if confirm.lower() == 'y':
                    sample_cards = [
                        ("What is Python?", "A high-level programming language", "Python Programming"),
                        ("What is a variable?", "A container for storing data values", "Python Programming"),
                        ("What is a function?", "A reusable block of code", "Python Programming"),
                        ("What is the capital of France?", "Paris", "General Knowledge"),
                        ("Who wrote Romeo and Juliet?", "William Shakespeare", "General Knowledge"),
                        ("What is 7 × 8?", "56", "Math"),
                        ("What is the square root of 144?", "12", "Math"),
                    ]
                    
                    for q, a, d in sample_cards:
                        deck.add_card(q, a, d)
                    
                    print(f"\n✓ Imported {len(sample_cards)} sample cards!")
            
            else:
                print("❌ Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled.")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
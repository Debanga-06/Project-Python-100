# Flashcards App (CLI) ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)

Professional command-line flashcard application with spaced repetition, progress tracking, and deck management for effective studying.

## Features

### Card Management
- **Create Cards**: Add custom question/answer pairs
- **Organize Decks**: Group cards by subject/topic
- **Search**: Find cards by keyword
- **Delete**: Remove unwanted cards
- **Import**: Load sample cards

### Study Modes
- **Normal Mode**: Question → Answer
- **Reverse Mode**: Answer → Question (for bidirectional learning)
- **Random Mix**: Mixed question/answer order
- **Targeted Review**: Focus on cards with low accuracy

### Progress Tracking
- **Study Statistics**: Times studied, correct, incorrect
- **Accuracy Percentage**: Track mastery level
- **Last Studied Date**: Monitor review schedule
- **Overall Progress**: Aggregate statistics

### Data Persistence
- **JSON Storage**: Cards saved automatically
- **Progress Saved**: All statistics preserved
- **Deck Organization**: Multiple topic support

## Requirements

- Python 3.x
- Built-in modules: `json`, `os`, `random`, `datetime`

## Installation

```bash
python flashcards_app.py
```

## Quick Start

### First Time Setup
```
==================================================
            FLASHCARDS APP (CLI)
==================================================

Main Menu:
  9. Import sample cards

Your choice: 9

✓ Imported 7 sample cards!
```

### Adding Your First Card
```
Your choice: 4

==================================================
ADD NEW FLASHCARD
==================================================

Question: What is the capital of Japan?
Answer: Tokyo
Deck name (default: General): Geography

✓ Card added to 'Geography' deck!
```

### Starting a Study Session
```
Your choice: 1

Study Mode:
  1. Normal (Question → Answer)
  2. Reverse (Answer → Question)
  3. Random Mix

Select mode (1-3, default 1): 1

==================================================
STUDY SESSION - 7 cards
==================================================

Card 1/7
----------------------------------------------------------------------

❓ Question: What is Python?

Press Enter to reveal answer

✅ Correct Answer: A high-level programming language

Did you get it right? (c=correct, i=incorrect): c
✓ Great job!
```

## Main Menu Options

### 1. Study All Cards
Study your entire card collection with randomized order.

**Features:**
- Shuffled card order
- Choice of study mode
- Self-assessment (correct/incorrect)
- Session summary with accuracy

**Example Session:**
```
==================================================
SESSION SUMMARY
==================================================
Cards Studied:   10
Correct:         8
Incorrect:       2
Accuracy:        80.0%

⭐ Good work! You're getting there!
==================================================
```

### 2. Study Specific Deck
Focus on one subject area.

```
Available Decks:
  1. Python Programming (3 cards)
  2. General Knowledge (2 cards)
  3. Math (2 cards)

Select deck number: 1

Study Mode:
  1. Normal (Question → Answer)
  2. Reverse (Answer → Question)

Select mode (1-2, default 1): 1
```

### 3. Study Cards Needing Review
Focuses on cards with <75% accuracy.

```
📚 Found 3 cards needing review

[Study session begins with only weak cards]
```

### 4. Add New Card
Create custom flashcards.

```
Question: What is the speed of light?
Answer: 299,792,458 meters per second
Deck name (default: General): Physics

✓ Card added to 'Physics' deck!
```

### 5. View All Cards
Browse your entire collection organized by deck.

```
==================================================
PYTHON PROGRAMMING DECK (3)
==================================================

1. [Python Programming]
   Q: What is Python?
   A: A high-level programming language
   Accuracy: 100% | Studies: 5

2. [Python Programming]
   Q: What is a variable?
   A: A container for storing data values
   Accuracy: 80% | Studies: 5
```

### 6. Search Cards
Find cards containing specific keywords.

```
Enter search keyword: capital

==================================================
SEARCH RESULTS FOR 'CAPITAL' (2)
==================================================

1. [General Knowledge]
   Q: What is the capital of France?
   A: Paris
   Accuracy: 100% | Studies: 3
```

### 7. Delete Card
Remove unwanted flashcards.

```
Enter card number to delete: 3

Delete: 'What is 7 × 8?'? (y/n): y
✓ Card deleted.
```

### 8. View Statistics
Comprehensive progress overview.

```
==================================================
OVERALL STATISTICS
==================================================

📚 Card Collection:
   Total Cards:      15
   Studied:          12
   Not Yet Studied:  3
   Decks:            4

📊 Study Statistics:
   Total Reviews:    45
   Correct:          38
   Incorrect:        7
   Overall Accuracy: 84.4%

⚠️  Cards Needing Review: 2
   (Cards with <75% accuracy)

📦 Decks:
   General Knowledge: 5 cards
   Math: 3 cards
   Physics: 4 cards
   Python Programming: 3 cards
==================================================
```

### 9. Import Sample Cards
Load pre-made flashcards for quick start.

**Includes:**
- Python Programming (3 cards)
- General Knowledge (2 cards)
- Math (2 cards)

## Study Modes Explained

### Normal Mode (Question → Answer)
Traditional flashcard studying:
1. See the question
2. Think of the answer
3. Reveal the correct answer
4. Self-assess accuracy

**Best for:**
- Recall practice
- Exam preparation
- Memorization

### Reverse Mode (Answer → Question)
Backward learning:
1. See the answer
2. Think of the question
3. Reveal the correct question
4. Self-assess accuracy

**Best for:**
- Recognition practice
- Vocabulary (word → definition AND definition → word)
- Bidirectional learning

### Random Mix
Randomly alternates between normal and reverse:
- Keeps you alert
- Prevents pattern memorization
- More challenging

## Progress Tracking

### Card Statistics
Each card tracks:
- **Times Studied**: Total study sessions
- **Times Correct**: Successful recalls
- **Times Incorrect**: Failed recalls
- **Accuracy**: Success rate percentage
- **Last Studied**: Most recent review date

### Performance Ratings

| Accuracy | Rating | Meaning |
|----------|--------|---------|
| 90-100% | 🌟 Excellent | Mastered |
| 75-89% | ⭐ Good | Well-learned |
| 60-74% | ✨ Improving | Needs practice |
| < 60% | 📚 Review | Requires study |

### Spaced Repetition Logic
Cards with <75% accuracy are flagged for review:
- Appear in "Cards Needing Review" list
- Prioritized for study sessions
- Helps focus on weak areas

## File Structure

### flashcards.json
Cards are saved in JSON format:

```json
[
  {
    "id": "card_20241228143052123456",
    "question": "What is Python?",
    "answer": "A high-level programming language",
    "deck_name": "Python Programming",
    "times_studied": 5,
    "times_correct": 5,
    "times_incorrect": 0,
    "last_studied": "2024-12-28T14:30:52.123456",
    "created_at": "2024-12-28T10:15:30.123456"
  }
]
```

## Use Cases

### Academic Study
- **Exam Preparation**: Memorize key concepts
- **Vocabulary**: Language learning
- **Definitions**: Technical terms
- **Formulas**: Math and science
- **Dates**: Historical events

### Professional Development
- **Certifications**: Study for IT certifications
- **Interview Prep**: Technical questions
- **Industry Knowledge**: Terms and concepts
- **Compliance**: Regulations and policies

### Personal Learning
- **Hobbies**: Learn new skills
- **Trivia**: General knowledge
- **Languages**: Word pairs and phrases
- **Cooking**: Recipe memorization
- **Music**: Theory and notation

## Study Tips

### Creating Effective Flashcards

#### Do's ✅
- **Be Specific**: One concept per card
- **Use Simple Language**: Clear and concise
- **Include Context**: When necessary
- **Focus on Understanding**: Not just memorization
- **Use Examples**: When helpful

#### Don'ts ❌
- **Avoid Complexity**: Multiple questions in one
- **Don't Be Vague**: "Explain X" is too broad
- **Skip Long Answers**: Break into multiple cards
- **Avoid Ambiguity**: Answers should be clear

### Examples

**Good Card:**
```
Q: What is the capital of France?
A: Paris
```

**Better Card:**
```
Q: What is the capital and largest city of France?
A: Paris
```

**Poor Card:**
```
Q: Tell me about France
A: France is a country in Europe with Paris as capital, 
   67 million people, and known for wine and cheese...
```

### Effective Study Strategies

#### 1. Spaced Repetition
- Study cards multiple times over increasing intervals
- Review weak cards more frequently
- Mastered cards less often

#### 2. Active Recall
- Try to answer before revealing
- Don't just recognize - actively remember
- Say answer out loud

#### 3. Regular Sessions
- **Daily practice**: 10-20 minutes
- **Consistent schedule**: Same time each day
- **Short sessions**: Better than cramming

#### 4. Mix Topics
- Don't study same deck repeatedly
- Alternate between subjects
- Prevents boredom and improves retention

#### 5. Test Yourself Honestly
- Be strict with self-assessment
- Mark unclear answers as incorrect
- Better to overestimate difficulty

## Advanced Features

### Deck Organization
Organize cards by:
- **Subject**: Math, Science, History
- **Course**: CS101, Biology 201
- **Difficulty**: Beginner, Intermediate, Advanced
- **Priority**: High, Medium, Low
- **Source**: Book chapters, lectures

### Search Functionality
Find cards containing:
- Keywords in questions
- Keywords in answers
- Specific topics
- Related concepts

**Example:**
```
Search: "capital"
Results: All cards with "capital" in Q or A
```

## Code Structure

### Classes

```python
class Flashcard:
    # Properties
    id, question, answer, deck_name
    times_studied, times_correct, times_incorrect
    last_studied, created_at
    
    # Methods
    study(correct)          # Record result
    get_accuracy()          # Calculate %
    to_dict()               # JSON export
    from_dict(data)         # JSON import

class FlashcardDeck:
    # Properties
    filename, cards
    
    # Methods
    load_cards()            # Load from file
    save_cards()            # Save to file
    add_card(q, a, deck)    # Create new
    remove_card(id)         # Delete
    get_cards_by_deck(name) # Filter by deck
    get_cards_needing_review() # Low accuracy
    search_cards(keyword)   # Search
```

### Main Functions

```python
study_session(deck, cards, mode)
# Conducts study session with given cards

display_statistics(deck)
# Shows overall progress

list_cards(cards, title)
# Displays card list

display_card_details(card)
# Shows full card info
```

## Data Backup

### Manual Backup
```bash
# Copy flashcards.json to backup location
cp flashcards.json flashcards_backup.json
```

### Restore from Backup
```bash
# Replace current file with backup
cp flashcards_backup.json flashcards.json
```

## Troubleshooting

### Cards Not Saving
- Check file permissions
- Ensure disk space available
- Verify JSON file not corrupted

### Statistics Not Updating
- Ensure you complete study sessions
- Don't quit mid-session
- Check file write permissions

### Missing Cards
- Verify correct file location
- Check for backup file
- Ensure JSON format valid

## Performance Benchmarks

### Recommended Card Limits
- **Per Deck**: 20-50 cards (manageable)
- **Total Collection**: 100-500 cards (effective)
- **Daily Review**: 20-30 cards (sustainable)

### Study Session Length
- **Beginner**: 10-15 minutes (5-10 cards)
- **Intermediate**: 15-25 minutes (10-20 cards)
- **Advanced**: 25-40 minutes (20-40 cards)

## Future Enhancements

- [ ] Multiple choice mode
- [ ] Image support
- [ ] Audio pronunciation
- [ ] Collaborative decks
- [ ] Import/export CSV
- [ ] Cloud sync
- [ ] Mobile app version
- [ ] Gamification (streaks, points)
- [ ] AI-generated hints
- [ ] Markdown support in cards

## Educational Benefits

### Cognitive Science Principles
- **Active Recall**: Strengthens memory
- **Spaced Repetition**: Optimal timing
- **Interleaving**: Mixed practice
- **Testing Effect**: Retrieval practice

### Learning Advantages
- Self-paced learning
- Immediate feedback
- Progress tracking
- Focused practice
- Portable study tool

## License

Free to use and modify for educational purposes.

## Credits

Built following cognitive science principles of effective learning and memory retention.
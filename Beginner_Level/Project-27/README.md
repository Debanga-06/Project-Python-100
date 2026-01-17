# Text Analyzer  ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)

A comprehensive Python text analysis tool that provides detailed statistics about text files, demonstrates string manipulation methods, file I/O operations, and statistical calculations.

## 📋 Features

### String Methods Demonstrated
- Character type detection (letters, digits, spaces, punctuation)
- Case conversion and analysis (upper/lower case counting)
- String translation and cleaning
- Text splitting and joining
- Pattern finding and searching

### File Operations
- Read text files with proper encoding
- Error handling for missing files
- Support for UTF-8 encoding
- Safe file operations

### Statistical Analysis
- **Character Statistics**: Total characters, letters, digits, spaces, punctuation
- **Word Statistics**: Word count, unique words, average length, median, standard deviation
- **Sentence Statistics**: Sentence count, average words per sentence
- **Word Frequency**: Most common words with occurrence counts
- **Readability Score**: Simple readability metrics with reading level assessment
- **Search Functionality**: Find word occurrences and positions

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only standard library)

### Setup
1. Clone or download the project:
```bash
git clone <your-repo-url>
cd text-analyzer
```

2. No additional installation needed - uses Python standard library only!

## 💻 Usage

### Basic Usage

Run the program:
```bash
python text_analyzer.py
```

### Menu Options

The program provides an interactive menu:

1. **Analyze Sample Text** - Analyze built-in sample text
2. **Load Text from File** - Analyze a text file
3. **Enter Custom Text** - Type or paste your own text
4. **Search for a Word** - Search for specific words in loaded text
5. **Exit** - Quit the program

### Example: Analyzing a File

1. Create a sample text file:
```bash
echo "Python is amazing. It makes programming fun and easy!" > sample.txt
```

2. Run the analyzer:
```bash
python text_analyzer.py
```

3. Select option 2 and enter `sample.txt`

### Example: Using as a Module

You can also import and use the TextAnalyzer class in your own code:

```python
from text_analyzer import TextAnalyzer

# Create analyzer instance
analyzer = TextAnalyzer()

# Load text from file
analyzer.load_from_file('myfile.txt')

# Or load from string
analyzer.load_from_string("Your text here")

# Get statistics
char_stats = analyzer.character_stats()
word_stats = analyzer.word_stats()
top_words = analyzer.word_frequency(5)

# Generate full report
analyzer.generate_report()

# Search for a word
result = analyzer.search_word("python")
print(f"Found {result['count']} occurrences")
```

## 📊 Sample Output

```
============================================================
                   TEXT ANALYSIS REPORT                    
============================================================

📝 CHARACTER STATISTICS:
   Total characters: 245
   Letters: 195
   Digits: 0
   Spaces: 42
   Punctuation: 8
   Uppercase: 5
   Lowercase: 190

📚 WORD STATISTICS:
   Total words: 42
   Unique words: 35
   Average word length: 4.64 chars
   Median word length: 4.0 chars
   Longest word: 'programming' (11 chars)
   Shortest word: 'is' (2 chars)

📄 SENTENCE STATISTICS:
   Total sentences: 5
   Avg words per sentence: 8.40
   Longest sentence: 12 words
   Shortest sentence: 4 words

🔥 TOP 10 MOST COMMON WORDS:
   'python': 3 times
   'the': 2 times
   'and': 2 times
   ...

📊 READABILITY:
   Score: 8.45
   Reading Level: Middle School

============================================================
```

## 🔧 Class Methods Reference

### TextAnalyzer Class

#### Loading Methods
- `load_from_file(filename)` - Load text from a file
- `load_from_string(text)` - Load text from a string

#### Analysis Methods
- `character_stats()` - Returns dictionary with character statistics
- `word_stats()` - Returns dictionary with word statistics
- `sentence_stats()` - Returns dictionary with sentence statistics
- `word_frequency(top_n)` - Returns list of most common words
- `search_word(word)` - Search for a word and return statistics
- `readability_score()` - Calculate readability metrics
- `generate_report()` - Print comprehensive analysis report

## 📁 Project Structure

```
text-analyzer/
├── text_analyzer.py    # Main program file
├── README.md          # This file
└── sample.txt         # Sample text file (optional)
```

## 🎓 Educational Purpose

This project demonstrates:

1. **String Methods**: `isalpha()`, `isdigit()`, `isspace()`, `upper()`, `lower()`, `split()`, `join()`, `translate()`, `replace()`, `find()`, `count()`

2. **File I/O**: `open()`, `read()`, error handling with try-except, encoding management

3. **Statistics Module**: `mean()`, `median()`, `stdev()`

4. **Collections**: `Counter` for frequency analysis, `Set` for unique elements

5. **Best Practices**: Error handling, clean code structure, documentation, user-friendly interface

## 🛠️ Customization

### Adding New Analysis Features

You can extend the `TextAnalyzer` class with new methods:

```python
def vowel_count(self):
    """Count vowels in text"""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in self.text if char in vowels)
```

### Modifying Word Frequency Filters

In the `word_frequency()` method, adjust the filter:

```python
# Change minimum word length
meaningful_words = [w for w in self.words if len(w) > 3]
```

## 🐛 Troubleshooting

**File not found error:**
- Ensure the file path is correct
- Check file permissions
- Verify file exists in the current directory

**Encoding errors:**
- The program uses UTF-8 encoding by default
- For other encodings, modify the `open()` call in `load_from_file()`

**Empty statistics:**
- Ensure text is loaded before analysis
- Check that the text file is not empty

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests. Suggestions for improvements are welcome!

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Happy Analyzing! 📊✨**
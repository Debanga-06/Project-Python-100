# Text Analyzer

A Python script that analyzes text files using string methods, file reading, and statistics.

## Features

- Counts total characters, words, and sentences in a text file
- Calculates statistics on word lengths (mean, median, mode)
- Handles file not found errors gracefully
- Automatically finds the input file relative to the script's location

## Requirements

- Python 3.8+
- `statistics` module (built-in)

## Usage

1. Place your text file as `input.txt` in the same directory as `text.py`
2. Run the script from anywhere:

```bash
python text.py
```

Or from the project directory:

```bash
python Beginner_Level/Project-27/text.py
```

## Example Output

```
Total Characters: 320
Total Words: 51
Total Sentences: 5
Mean Word Length: 5.29
Median Word Length: 4
Mode Word Length: 4
```

## Key Concepts Demonstrated

- **File Reading**: Using `open()` and `read()` to load text files
- **String Methods**: `lower()`, `split()`, `strip()` for text processing
- **Statistics**: Using the `statistics` module for data analysis
- **Path Handling**: Using `os.path` to locate files relative to the script</content>
<parameter name="filePath">c:\Users\Jiban Maji\OneDrive\Desktop\VS CODE\Project-Python-100\Beginner_Level\Project-27\README.md
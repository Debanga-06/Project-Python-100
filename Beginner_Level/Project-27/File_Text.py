"""
Text Analyzer - String Methods, File Reading, and Statistics
Analyzes text files and provides comprehensive statistics
"""

import string
import statistics
from collections import Counter
import os


class TextAnalyzer:
    def __init__(self, text=""):
        self.text = text
        self.words = []
        self.sentences = []
        
    def load_from_file(self, filename):
        """Read text from a file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                self.text = file.read()
            print(f"✓ Successfully loaded '{filename}'")
            return True
        except FileNotFoundError:
            print(f"✗ Error: File '{filename}' not found")
            return False
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return False
    
    def load_from_string(self, text):
        """Load text from a string"""
        self.text = text
    
    def _prepare_words(self):
        """Extract and clean words from text"""
        # Remove punctuation and convert to lowercase
        translator = str.maketrans('', '', string.punctuation)
        cleaned = self.text.translate(translator)
        self.words = cleaned.lower().split()
    
    def _prepare_sentences(self):
        """Split text into sentences"""
        # Simple sentence splitting by common sentence endings
        text = self.text.replace('!', '.').replace('?', '.')
        self.sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    def character_stats(self):
        """Analyze character statistics"""
        total_chars = len(self.text)
        letters = sum(c.isalpha() for c in self.text)
        digits = sum(c.isdigit() for c in self.text)
        spaces = sum(c.isspace() for c in self.text)
        punctuation = sum(c in string.punctuation for c in self.text)
        uppercase = sum(c.isupper() for c in self.text)
        lowercase = sum(c.islower() for c in self.text)
        
        return {
            'total': total_chars,
            'letters': letters,
            'digits': digits,
            'spaces': spaces,
            'punctuation': punctuation,
            'uppercase': uppercase,
            'lowercase': lowercase
        }
    
    def word_stats(self):
        """Analyze word statistics"""
        self._prepare_words()
        
        if not self.words:
            return None
        
        word_lengths = [len(word) for word in self.words]
        
        return {
            'total_words': len(self.words),
            'unique_words': len(set(self.words)),
            'avg_length': statistics.mean(word_lengths),
            'median_length': statistics.median(word_lengths),
            'longest_word': max(self.words, key=len),
            'shortest_word': min(self.words, key=len),
            'std_dev': statistics.stdev(word_lengths) if len(word_lengths) > 1 else 0
        }
    
    def sentence_stats(self):
        """Analyze sentence statistics"""
        self._prepare_sentences()
        
        if not self.sentences:
            return None
        
        sentence_lengths = [len(s.split()) for s in self.sentences]
        
        return {
            'total_sentences': len(self.sentences),
            'avg_words_per_sentence': statistics.mean(sentence_lengths),
            'longest_sentence_words': max(sentence_lengths),
            'shortest_sentence_words': min(sentence_lengths)
        }
    
    def word_frequency(self, top_n=10):
        """Get most common words"""
        self._prepare_words()
        
        # Filter out very short words
        meaningful_words = [w for w in self.words if len(w) > 2]
        
        counter = Counter(meaningful_words)
        return counter.most_common(top_n)
    
    def search_word(self, word):
        """Search for a word and return statistics"""
        word_lower = word.lower()
        count = self.text.lower().count(word_lower)
        
        # Find positions
        positions = []
        start = 0
        while True:
            pos = self.text.lower().find(word_lower, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return {
            'word': word,
            'count': count,
            'positions': positions
        }
    
    def readability_score(self):
        """Calculate simple readability metrics"""
        word_stat = self.word_stats()
        sent_stat = self.sentence_stats()
        
        if not word_stat or not sent_stat:
            return None
        
        # Simple readability estimate
        avg_word_len = word_stat['avg_length']
        avg_sent_len = sent_stat['avg_words_per_sentence']
        
        score = (4.71 * avg_word_len) + (0.5 * avg_sent_len) - 21.43
        
        return {
            'score': max(0, score),
            'level': self._get_reading_level(score)
        }
    
    def _get_reading_level(self, score):
        """Determine reading level from score"""
        if score < 6:
            return "Elementary"
        elif score < 10:
            return "Middle School"
        elif score < 13:
            return "High School"
        else:
            return "College"
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        print("\n" + "="*60)
        print("TEXT ANALYSIS REPORT".center(60))
        print("="*60)
        
        # Character Statistics
        char_stats = self.character_stats()
        print("\n📝 CHARACTER STATISTICS:")
        print(f"   Total characters: {char_stats['total']}")
        print(f"   Letters: {char_stats['letters']}")
        print(f"   Digits: {char_stats['digits']}")
        print(f"   Spaces: {char_stats['spaces']}")
        print(f"   Punctuation: {char_stats['punctuation']}")
        print(f"   Uppercase: {char_stats['uppercase']}")
        print(f"   Lowercase: {char_stats['lowercase']}")
        
        # Word Statistics
        word_stats = self.word_stats()
        if word_stats:
            print("\n📚 WORD STATISTICS:")
            print(f"   Total words: {word_stats['total_words']}")
            print(f"   Unique words: {word_stats['unique_words']}")
            print(f"   Average word length: {word_stats['avg_length']:.2f} chars")
            print(f"   Median word length: {word_stats['median_length']:.1f} chars")
            print(f"   Longest word: '{word_stats['longest_word']}' ({len(word_stats['longest_word'])} chars)")
            print(f"   Shortest word: '{word_stats['shortest_word']}' ({len(word_stats['shortest_word'])} chars)")
        
        # Sentence Statistics
        sent_stats = self.sentence_stats()
        if sent_stats:
            print("\n📄 SENTENCE STATISTICS:")
            print(f"   Total sentences: {sent_stats['total_sentences']}")
            print(f"   Avg words per sentence: {sent_stats['avg_words_per_sentence']:.2f}")
            print(f"   Longest sentence: {sent_stats['longest_sentence_words']} words")
            print(f"   Shortest sentence: {sent_stats['shortest_sentence_words']} words")
        
        # Word Frequency
        print("\n🔥 TOP 10 MOST COMMON WORDS:")
        for word, count in self.word_frequency(10):
            print(f"   '{word}': {count} times")
        
        # Readability
        readability = self.readability_score()
        if readability:
            print("\n📊 READABILITY:")
            print(f"   Score: {readability['score']:.2f}")
            print(f"   Reading Level: {readability['level']}")
        
        print("\n" + "="*60)


def main():
    """Main function to demonstrate the text analyzer"""
    
    print("=" * 60)
    print("TEXT ANALYZER - Python Project".center(60))
    print("=" * 60)
    
    # Sample text for demonstration
    sample_text = """
    Python is a powerful programming language. It is widely used for 
    data analysis, web development, and artificial intelligence. 
    Python's syntax is clean and easy to read. Many developers love 
    Python because it allows them to write code quickly and efficiently.
    The Python community is large and supportive. Python continues to 
    grow in popularity every year!
    """
    
    # Create analyzer instance
    analyzer = TextAnalyzer()
    
    # Menu system
    while True:
        print("\n" + "-" * 60)
        print("OPTIONS:")
        print("1. Analyze sample text")
        print("2. Load text from file")
        print("3. Enter custom text")
        print("4. Search for a word")
        print("5. Exit")
        print("-" * 60)
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            analyzer.load_from_string(sample_text)
            analyzer.generate_report()
            
        elif choice == '2':
            filename = input("Enter filename: ").strip()
            if analyzer.load_from_file(filename):
                analyzer.generate_report()
                
        elif choice == '3':
            print("Enter your text (type 'END' on a new line when done):")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            custom_text = '\n'.join(lines)
            analyzer.load_from_string(custom_text)
            analyzer.generate_report()
            
        elif choice == '4':
            if not analyzer.text:
                print("⚠ Please load text first!")
                continue
            word = input("Enter word to search: ").strip()
            result = analyzer.search_word(word)
            print(f"\n🔍 Search Results for '{result['word']}':")
            print(f"   Found {result['count']} occurrence(s)")
            if result['positions']:
                print(f"   Positions: {result['positions'][:5]}" + 
                      (" ..." if len(result['positions']) > 5 else ""))
                
        elif choice == '5':
            print("\n✓ Thank you for using Text Analyzer!")
            break
            
        else:
            print("⚠ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
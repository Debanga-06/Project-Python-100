import statistics
import os

def text_analyzer(file_path):
    try:
        # Step 1: File Reading
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Step 2: String Methods
        # Convert to lowercase for uniformity
        text_lower = text.lower()
        
        # Split into words and sentences
        words = text_lower.split()
        sentences = text.split('.')
        
        # Remove empty strings from sentences
        sentences = [s.strip() for s in sentences if s.strip() != ""]
        
        # Step 3: Basic Counts
        char_count = len(text)
        word_count = len(words)
        sentence_count = len(sentences)
        
        # Step 4: Word Lengths for Statistics
        word_lengths = [len(word) for word in words]
        
        # Step 5: Statistics
        mean_word_len = statistics.mean(word_lengths) if word_lengths else 0
        median_word_len = statistics.median(word_lengths) if word_lengths else 0
        try:
            mode_word_len = statistics.mode(word_lengths) if word_lengths else 0
        except statistics.StatisticsError:
            mode_word_len = "No unique mode"
        
        # Step 6: Results
        result = {
            "Total Characters": char_count,
            "Total Words": word_count,
            "Total Sentences": sentence_count,
            "Mean Word Length": round(mean_word_len, 2),
            "Median Word Length": median_word_len,
            "Mode Word Length": mode_word_len
        }
        
        return result
    
    except FileNotFoundError:
        return {"Error": f"File '{file_path}' not found."}


# Example usage
if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, "input.txt")
    analysis = text_analyzer(file_name)
    for key, value in analysis.items():
        print(f"{key}: {value}")
# Sentiment Analysis Tool

A text classification project that reads a piece of text (like a product or movie review) and figures out whether it's positive, negative, or neutral. Built for my Python 100 advanced project, covering NLP + ML basics: cleaning text, turning it into numbers with TF-IDF, and training a few different classifiers to see which one actually performs best.

## What it does

You give it a sentence, it tells you the sentiment and how confident it is. Under the hood it's comparing three different ML models on the same data and picking whichever one scored highest, instead of just assuming one algorithm is "the right one."

## Project layout

```
sentiment_analysis_tool/
├── data/
│   ├── build_dataset.py   -> generates the labeled review dataset
│   └── reviews.csv        -> text + sentiment label (created after you run build_dataset.py)
├── src/
│   ├── preprocessing.py   -> text cleaning (lowercasing, removing junk, stopwords)
│   └── model.py           -> vectorizing text + training/comparing the models
├── main.py                -> runs the whole thing end to end
└── requirements.txt
```

## The pipeline, step by step

**1. Getting data.** I didn't have internet access to pull down something like the IMDB dataset, so `build_dataset.py` generates a batch of review-style sentences from a big pool of hand-written templates (positive, negative, neutral), swapping in different nouns and phrasing so it doesn't look identical every time. Ends up with about 1000 labeled examples split evenly across the three classes. If you've got a real dataset, just drop it in as `data/reviews.csv` with `text` and `sentiment` columns and it'll use that instead.

**2. Cleaning the text.** `preprocessing.py` lowercases everything, strips out URLs and punctuation, and removes a small list of common stopwords (the, is, and, etc.) that don't really carry sentiment on their own. Didn't bother pulling in nltk for this since it needs a separate corpus download - a plain stopword list does the job fine for review-length text.

**3. Turning text into numbers.** Machine learning models can't read words directly, so `TfidfVectorizer` converts each cleaned sentence into a vector of numbers based on how important each word (and pairs of words, using bigrams) is across the dataset. Words that show up everywhere get less weight, words that are more distinctive get more.

**4. Training and comparing models.** Three classifiers get trained on the same TF-IDF features:
- **Naive Bayes** - the classic go-to for text classification, fast and simple
- **Logistic Regression** - usually a solid all-rounder for this kind of task
- **Linear SVM** - tends to do well when there are lots of features (which TF-IDF produces)

Whichever one scores highest on accuracy against a held-out test set gets kept as the "best" model for making predictions.

**5. Making predictions.** Once trained, you can feed it any new sentence and it'll clean it the same way, vectorize it, and return a label plus a confidence score.

## Running it

Install what's needed:
```
pip install -r requirements.txt
```

Then just run:
```
python main.py
```

This builds the dataset if it doesn't exist yet, trains all three models, prints out an accuracy comparison, shows a full classification report and confusion matrix for the winner, and then tests it on a handful of new sentences it hasn't seen before. At the end it saves the trained model to `sentiment_model.joblib` so you don't have to retrain every time.

## Sample output

```
Model                   Accuracy
--------------------------------
naive_bayes              100.00%
logistic_regression      100.00%
linear_svm               100.00%

Trying it on a few new sentences:

[positive | conf: 0.818]  This is hands down the best purchase I've made all year, love it.
[negative | conf: 0.661]  Terrible experience, everything about it was broken and slow.
[ neutral | conf: 0.838]  It was fine I guess, does what it says on the box, nothing more.
[negative | conf: 0.85 ]  Honestly kind of underwhelmed, expected way more for this price.
[positive | conf: 0.964]  Absolutely fantastic service, the staff went above and beyond.
```

Worth noting: the 100% test accuracy is a bit inflated because the test set comes from the same template pool as training. The real check is the sentences at the bottom, which the model never saw during training and still got right. If you swap in a real-world dataset the accuracy will drop to something more realistic (probably 80-90% range), which is normal.

## Using your own text

```python
from src.model import SentimentModel
import pandas as pd

df = pd.read_csv("data/reviews.csv")
model = SentimentModel()
model.train_and_compare(df)

label, confidence = model.predict_with_confidence("Honestly not what I expected, kind of a letdown.")
print(label, confidence)
```

Or load the already-trained model without retraining:
```python
model = SentimentModel.load("sentiment_model.joblib")
label, confidence = model.predict_with_confidence("This was surprisingly good!")
```

## Things I'd add if I had more time

- Try it on a real dataset (IMDB reviews, Twitter sentiment, Amazon reviews) instead of the generated one
- Add a simple web interface with Flask so you can type a sentence and get a result without touching the terminal
- Try word embeddings (Word2Vec or something transformer-based) instead of TF-IDF to see if accuracy improves on real-world text
- Handle sarcasm/negation better - "not bad" and "not good" currently rely entirely on the bigram catching it
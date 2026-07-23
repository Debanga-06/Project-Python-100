import os
import pandas as pd

from src.model import SentimentModel

DATA_PATH = os.path.join("data", "reviews.csv")


def load_data():
    if not os.path.exists(DATA_PATH):
        print("No dataset found yet, building one now...\n")
        from data.build_dataset import build_dataset
        df = build_dataset(n_per_class=350)
        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
    else:
        df = pd.read_csv(DATA_PATH)
    return df


def print_comparison(results):
    print(f"{'Model':<22}{'Accuracy':>10}")
    print("-" * 32)
    for name, res in sorted(results.items(), key=lambda x: -x[1]["accuracy"]):
        print(f"{name:<22}{res['accuracy']*100:>9.2f}%")


def main():
    df = load_data()
    print(f"Loaded {len(df)} labeled reviews.")
    print(df["sentiment"].value_counts().to_string())

    model = SentimentModel(max_features=5000, ngram_range=(1, 2))
    results = model.train_and_compare(df)

    print("\nModel comparison (held-out test set):\n")
    print_comparison(results)

    best = model.best_model_name
    print(f"\nBest performing model: {best}")
    print("\nDetailed report for the best model:\n")
    print(results[best]["report"])

    print("Confusion matrix (rows = actual, columns = predicted):")
    labels = results[best]["labels"]
    print("labels order:", labels)
    print(results[best]["confusion_matrix"])

    # quick sanity check on sentences the model has never seen
    sample_sentences = [
        "This is hands down the best purchase I've made all year, love it.",
        "Terrible experience, everything about it was broken and slow.",
        "It was fine I guess, does what it says on the box, nothing more.",
        "Honestly kind of underwhelmed, expected way more for this price.",
        "Absolutely fantastic service, the staff went above and beyond.",
    ]

    print("\nTrying it on a few new sentences:\n")
    for s in sample_sentences:
        label, confidence = model.predict_with_confidence(s)
        print(f"[{label:>8} | conf: {confidence}]  {s}")

    model.save("sentiment_model.joblib")
    print("\nSaved trained model to sentiment_model.joblib")


if __name__ == "__main__":
    main()

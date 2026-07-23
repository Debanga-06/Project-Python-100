import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from src.preprocessing import clean_series


class SentimentModel:
    def __init__(self, max_features=5000, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features, ngram_range=ngram_range, min_df=2
        )
        self.models = {
            "naive_bayes": MultinomialNB(),
            "logistic_regression": LogisticRegression(max_iter=1000),
            "linear_svm": LinearSVC(),
        }
        self.best_model_name = None
        self.best_model = None
        self.is_fitted = False

    def prepare_data(self, df: pd.DataFrame, text_col="text", label_col="sentiment", test_size=0.2):
        cleaned = clean_series(df[text_col])
        X_train_raw, X_test_raw, y_train, y_test = train_test_split(
            cleaned, df[label_col], test_size=test_size, random_state=42, stratify=df[label_col]
        )
        X_train = self.vectorizer.fit_transform(X_train_raw)
        X_test = self.vectorizer.transform(X_test_raw)
        return X_train, X_test, y_train, y_test

    def train_and_compare(self, df: pd.DataFrame, text_col="text", label_col="sentiment"):
        """Trains every model in self.models, prints a comparison, keeps the best one."""
        X_train, X_test, y_train, y_test = self.prepare_data(df, text_col, label_col)

        results = {}
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            results[name] = {
                "accuracy": acc,
                "report": classification_report(y_test, preds, zero_division=0),
                "confusion_matrix": confusion_matrix(y_test, preds, labels=sorted(y_test.unique())),
                "labels": sorted(y_test.unique()),
            }

        self.best_model_name = max(results, key=lambda k: results[k]["accuracy"])
        self.best_model = self.models[self.best_model_name]
        self.is_fitted = True

        return results

    def predict(self, texts):
        """Predict sentiment for a list of raw (uncleaned) strings using the best model found so far."""
        if not self.is_fitted:
            raise RuntimeError("Call train_and_compare() first.")

        cleaned = clean_series(texts)
        X = self.vectorizer.transform(cleaned)
        return self.best_model.predict(X)

    def predict_with_confidence(self, text: str):
        """
        Returns (label, confidence). Logistic regression exposes real
        probabilities out of the box - LinearSVC and MultinomialNB get a
        rough proxy from decision_function / predict_proba where available.
        """
        if not self.is_fitted:
            raise RuntimeError("Call train_and_compare() first.")

        cleaned = clean_series([text])
        X = self.vectorizer.transform(cleaned)
        label = self.best_model.predict(X)[0]

        if hasattr(self.best_model, "predict_proba"):
            probs = self.best_model.predict_proba(X)[0]
            confidence = float(np.max(probs))
        elif hasattr(self.best_model, "decision_function"):
            scores = self.best_model.decision_function(X)[0]
            scores = np.atleast_1d(scores)
            confidence = float(1 / (1 + np.exp(-np.max(np.abs(scores)))))
        else:
            confidence = 1.0

        return label, round(confidence, 3)

    def save(self, path="sentiment_model.joblib"):
        joblib.dump({
            "vectorizer": self.vectorizer,
            "best_model": self.best_model,
            "best_model_name": self.best_model_name,
        }, path)

    @classmethod
    def load(cls, path="sentiment_model.joblib"):
        data = joblib.load(path)
        instance = cls()
        instance.vectorizer = data["vectorizer"]
        instance.best_model = data["best_model"]
        instance.best_model_name = data["best_model_name"]
        instance.is_fitted = True
        return instance

"""
content_based.py
------------------
Content-Based Filtering recommender.

Builds a TF-IDF representation of each movie from its genres + description,
then recommends movies most similar (cosine similarity) to a movie the user
already liked. This approach does not need any other users' data -- it works
purely from item metadata, so it also solves the "new user" cold-start problem.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    def __init__(self, movies_df: pd.DataFrame):
        self.movies_df = movies_df.reset_index(drop=True)
        self._title_to_index = pd.Series(
            self.movies_df.index, index=self.movies_df["title"]
        )
        self._tfidf_matrix = None
        self._similarity_matrix = None

    def fit(self):
        """Builds the TF-IDF matrix and the item-item cosine similarity matrix."""
        combined_features = (
            # Genres weighted more heavily by repeating them -- genre match
            # matters more than shared words in a free-text description.
            (self.movies_df["genres"].str.replace("|", " ", regex=False) + " ") * 2
            + self.movies_df["description"]
        )

        vectorizer = TfidfVectorizer(stop_words="english")
        self._tfidf_matrix = vectorizer.fit_transform(combined_features)
        self._similarity_matrix = cosine_similarity(self._tfidf_matrix)
        return self

    def recommend(self, title: str, top_n: int = 10) -> pd.DataFrame:
        """Return the top_n movies most similar to `title`."""
        if self._similarity_matrix is None:
            raise RuntimeError("Call .fit() before .recommend().")

        if title not in self._title_to_index:
            raise ValueError(f"'{title}' not found in the movie catalogue.")

        idx = self._title_to_index[title]
        scores = list(enumerate(self._similarity_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx][:top_n]

        result_indices = [i for i, _ in scores]
        result = self.movies_df.iloc[result_indices][["movie_id", "title", "genres"]].copy()
        result["similarity_score"] = [round(s, 4) for _, s in scores]
        return result.reset_index(drop=True)

    def recommend_for_profile(self, liked_titles: list, top_n: int = 10) -> pd.DataFrame:
        """
        Recommend movies based on a user's *profile* built from several
        liked movies at once (average of their TF-IDF vectors), rather
        than just one seed movie.
        """
        indices = [self._title_to_index[t] for t in liked_titles if t in self._title_to_index]
        if not indices:
            raise ValueError("None of the provided titles were found in the catalogue.")

        profile_vector = np.asarray(self._tfidf_matrix[indices].mean(axis=0))
        scores = cosine_similarity(profile_vector, self._tfidf_matrix).flatten()

        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        ranked = [r for r in ranked if r[0] not in indices][:top_n]

        result_indices = [i for i, _ in ranked]
        result = self.movies_df.iloc[result_indices][["movie_id", "title", "genres"]].copy()
        result["similarity_score"] = [round(s, 4) for _, s in ranked]
        return result.reset_index(drop=True)

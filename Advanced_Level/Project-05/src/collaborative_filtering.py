"""
collaborative_filtering.py
----------------------------
Collaborative Filtering recommender with two strategies:

1. User-Based CF   -- finds users with similar taste (cosine similarity on
                       the user-item rating matrix) and recommends what
                       they liked.
2. Matrix Factorization (SVD) -- decomposes the sparse user-item matrix into
                       latent factors using Truncated SVD, then reconstructs
                       predicted ratings for every (user, movie) pair. This
                       is the same family of algorithm that powered the
                       winning entry of the Netflix Prize.

Both are implemented from the same underlying user-item matrix so they can
be compared directly, and combined in hybrid.py.
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class CollaborativeFilteringRecommender:
    def __init__(self, ratings_df: pd.DataFrame, movies_df: pd.DataFrame, n_factors: int = 20):
        self.ratings_df = ratings_df
        self.movies_df = movies_df
        self.n_factors = n_factors

        self.user_item_matrix = None
        self.user_means = None
        self.predicted_ratings = None
        self._user_ids = None
        self._movie_ids = None

    # ------------------------------------------------------------------
    # Matrix construction
    # ------------------------------------------------------------------
    def _build_matrix(self, ratings_df):
        matrix = ratings_df.pivot_table(
            index="user_id", columns="movie_id", values="rating"
        )
        return matrix

    def fit(self):
        """Builds the user-item matrix and fits the SVD latent-factor model."""
        self.user_item_matrix = self._build_matrix(self.ratings_df)
        self._user_ids = self.user_item_matrix.index.to_numpy()
        self._movie_ids = self.user_item_matrix.columns.to_numpy()

        # Mean-center each user's ratings, filling gaps with 0 (= user's mean)
        self.user_means = self.user_item_matrix.mean(axis=1)
        matrix_filled = self.user_item_matrix.sub(self.user_means, axis=0).fillna(0)

        n_factors = min(self.n_factors, min(matrix_filled.shape) - 1)
        svd = TruncatedSVD(n_components=n_factors, random_state=42)
        latent_users = svd.fit_transform(matrix_filled)
        reconstructed = latent_users.dot(svd.components_)

        self.predicted_ratings = pd.DataFrame(
            reconstructed, index=self.user_item_matrix.index,
            columns=self.user_item_matrix.columns
        ).add(self.user_means, axis=0)

        return self

    # ------------------------------------------------------------------
    # Matrix-factorization based recommendations
    # ------------------------------------------------------------------
    def recommend_svd(self, user_id: int, top_n: int = 10) -> pd.DataFrame:
        if self.predicted_ratings is None:
            raise RuntimeError("Call .fit() before recommending.")
        if user_id not in self.predicted_ratings.index:
            raise ValueError(f"user_id {user_id} not found in ratings data.")

        already_rated = self.user_item_matrix.loc[user_id].dropna().index
        predictions = self.predicted_ratings.loc[user_id].drop(index=already_rated)
        top_movie_ids = predictions.sort_values(ascending=False).head(top_n)

        result = self.movies_df.set_index("movie_id").loc[top_movie_ids.index][["title", "genres"]].copy()
        result["predicted_rating"] = top_movie_ids.values.round(2)
        return result.reset_index()

    # ------------------------------------------------------------------
    # User-based neighborhood recommendations
    # ------------------------------------------------------------------
    def recommend_user_based(self, user_id: int, top_n: int = 10, k_neighbors: int = 15) -> pd.DataFrame:
        if self.user_item_matrix is None:
            raise RuntimeError("Call .fit() before recommending.")
        if user_id not in self.user_item_matrix.index:
            raise ValueError(f"user_id {user_id} not found in ratings data.")

        filled = self.user_item_matrix.fillna(0)
        sims = cosine_similarity(filled)
        sims_df = pd.DataFrame(sims, index=filled.index, columns=filled.index)

        neighbor_scores = sims_df[user_id].drop(index=user_id)
        top_neighbors = neighbor_scores.sort_values(ascending=False).head(k_neighbors)

        neighbor_ratings = self.user_item_matrix.loc[top_neighbors.index]
        weights = top_neighbors.values.reshape(-1, 1)

        weighted_sum = (neighbor_ratings.fillna(0).values * weights).sum(axis=0)
        weight_totals = (neighbor_ratings.notna().values * weights).sum(axis=0)
        with np.errstate(invalid="ignore", divide="ignore"):
            scores = np.where(weight_totals > 0, weighted_sum / weight_totals, 0)

        scores_series = pd.Series(scores, index=self.user_item_matrix.columns)
        already_rated = self.user_item_matrix.loc[user_id].dropna().index
        scores_series = scores_series.drop(index=already_rated, errors="ignore")

        top_movie_ids = scores_series.sort_values(ascending=False).head(top_n)
        result = self.movies_df.set_index("movie_id").loc[top_movie_ids.index][["title", "genres"]].copy()
        result["predicted_rating"] = top_movie_ids.values.round(2)
        return result.reset_index()

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------
    def evaluate_rmse(self, test_size: float = 0.2, random_state: int = 42) -> float:
        """
        Holds out a fraction of the ratings, refits SVD on the remaining
        ratings, and reports RMSE between predicted and true ratings on
        the held-out set. Standard way to sanity-check a CF model.
        """
        train_df, test_df = train_test_split(
            self.ratings_df, test_size=test_size, random_state=random_state
        )

        temp_model = CollaborativeFilteringRecommender(train_df, self.movies_df, self.n_factors)
        temp_model.fit()

        preds, actuals = [], []
        for _, row in test_df.iterrows():
            user_id, movie_id, actual = row["user_id"], row["movie_id"], row["rating"]
            if user_id in temp_model.predicted_ratings.index and movie_id in temp_model.predicted_ratings.columns:
                pred = temp_model.predicted_ratings.loc[user_id, movie_id]
                preds.append(np.clip(pred, 1, 5))
                actuals.append(actual)

        if not preds:
            raise RuntimeError("No overlapping (user, movie) pairs between train and test sets.")

        rmse = np.sqrt(mean_squared_error(actuals, preds))
        return rmse

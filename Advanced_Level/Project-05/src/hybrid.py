"""
Hybrid recommender that blends Content-Based and Collaborative Filtering
scores into a single ranked list. This mitigates the weaknesses of each
approach on its own:

    - Content-based alone -> "filter bubble", only ever recommends
      near-duplicates of what the user already watched.
    - Collaborative alone -> cold-start problem for new users/movies with
      little or no rating history.

The hybrid score is a weighted sum:
    final_score = alpha * normalized_CF_score + (1 - alpha) * normalized_CB_score
"""

import numpy as np
import pandas as pd


class HybridRecommender:
    def __init__(self, content_model, collaborative_model, alpha: float = 0.6):
        self.content_model = content_model
        self.collaborative_model = collaborative_model
        self.alpha = alpha

    @staticmethod
    def _normalize(series: pd.Series) -> pd.Series:
        if series.max() == series.min():
            return series * 0
        return (series - series.min()) / (series.max() - series.min())

    def recommend(self, user_id: int, liked_titles: list, top_n: int = 10) -> pd.DataFrame:
        movies_df = self.content_model.movies_df

        # ---- Collaborative filtering scores (SVD-predicted ratings) ----
        already_rated = self.collaborative_model.user_item_matrix.loc[user_id].dropna().index
        cf_scores = self.collaborative_model.predicted_ratings.loc[user_id].drop(
            index=already_rated, errors="ignore"
        )

        # ---- Content-based scores (similarity to the user's liked movies) ----
        cb_result = self.content_model.recommend_for_profile(liked_titles, top_n=len(movies_df))
        cb_scores = cb_result.set_index("movie_id")["similarity_score"]

        # Align both score series on the same movie_id index
        all_ids = cf_scores.index.union(cb_scores.index)
        cf_scores = cf_scores.reindex(all_ids).fillna(cf_scores.mean())
        cb_scores = cb_scores.reindex(all_ids).fillna(0)

        cf_norm = self._normalize(cf_scores)
        cb_norm = self._normalize(cb_scores)

        final_scores = self.alpha * cf_norm + (1 - self.alpha) * cb_norm
        final_scores = final_scores.drop(index=already_rated, errors="ignore")
        top_ids = final_scores.sort_values(ascending=False).head(top_n)

        result = movies_df.set_index("movie_id").loc[top_ids.index][["title", "genres"]].copy()
        result["hybrid_score"] = top_ids.values.round(4)
        return result.reset_index()

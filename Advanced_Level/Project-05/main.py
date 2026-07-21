"""
main.py
--------
Entry point for the Movie Recommendation System.

Demonstrates:
    1. Content-Based Filtering  (TF-IDF + cosine similarity)
    2. Collaborative Filtering  (User-based CF and SVD matrix factorization)
    3. Hybrid Recommender       (weighted blend of both)

Run:
    python main.py
"""

import os
import pandas as pd

from src.content_based import ContentBasedRecommender
from src.collaborative_filtering import CollaborativeFilteringRecommender
from src.hybrid import HybridRecommender

DATA_DIR = "data"


def load_data():
    movies_path = os.path.join(DATA_DIR, "movies.csv")
    ratings_path = os.path.join(DATA_DIR, "ratings.csv")

    if not (os.path.exists(movies_path) and os.path.exists(ratings_path)):
        print("Dataset not found -- generating synthetic data first...\n")
        from data.generate_data import generate_movies, generate_ratings
        movies_df = generate_movies(n_movies=300)
        ratings_df = generate_ratings(movies_df, n_users=250)
        os.makedirs(DATA_DIR, exist_ok=True)
        movies_df.to_csv(movies_path, index=False)
        ratings_df.to_csv(ratings_path, index=False)
    else:
        movies_df = pd.read_csv(movies_path)
        ratings_df = pd.read_csv(ratings_path)

    return movies_df, ratings_df


def print_header(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def main():
    movies_df, ratings_df = load_data()
    print(f"Loaded {len(movies_df)} movies and {len(ratings_df)} ratings "
          f"from {ratings_df['user_id'].nunique()} users.")

    # ------------------------------------------------------------------
    # 1. Content-Based Filtering
    # ------------------------------------------------------------------
    print_header("1. CONTENT-BASED FILTERING")
    cb_model = ContentBasedRecommender(movies_df)
    cb_model.fit()

    seed_movie = movies_df.iloc[0]["title"]
    print(f"Movies similar to: '{seed_movie}'\n")
    print(cb_model.recommend(seed_movie, top_n=5).to_string(index=False))

    # ------------------------------------------------------------------
    # 2. Collaborative Filtering
    # ------------------------------------------------------------------
    print_header("2. COLLABORATIVE FILTERING")
    cf_model = CollaborativeFilteringRecommender(ratings_df, movies_df, n_factors=20)
    cf_model.fit()

    sample_user = int(ratings_df["user_id"].iloc[0])

    print(f"SVD (matrix factorization) recommendations for user {sample_user}:\n")
    print(cf_model.recommend_svd(sample_user, top_n=5).to_string(index=False))

    print(f"\nUser-based neighborhood recommendations for user {sample_user}:\n")
    print(cf_model.recommend_user_based(sample_user, top_n=5).to_string(index=False))

    print("\nEvaluating SVD model with train/test RMSE...")
    rmse = cf_model.evaluate_rmse(test_size=0.2)
    print(f"RMSE on held-out ratings: {rmse:.4f}  (scale is 1-5 stars)")

    # ------------------------------------------------------------------
    # 3. Hybrid Recommender
    # ------------------------------------------------------------------
    print_header("3. HYBRID RECOMMENDER (Content + Collaborative)")
    liked_titles = movies_df["title"].sample(3, random_state=1).tolist()
    print(f"User {sample_user} has liked: {liked_titles}\n")

    hybrid_model = HybridRecommender(cb_model, cf_model, alpha=0.6)
    hybrid_recs = hybrid_model.recommend(sample_user, liked_titles, top_n=5)
    print(hybrid_recs.to_string(index=False))

    print("\nDone. See README.md for a full explanation of each algorithm.")


if __name__ == "__main__":
    main()

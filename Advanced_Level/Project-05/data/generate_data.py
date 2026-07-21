"""
generate_data.py
-----------------
Generates a realistic synthetic movie catalogue and a user-ratings dataset
so the recommendation system can be run end-to-end without needing to
download an external dataset (e.g. MovieLens).

Running this script creates:
    data/movies.csv   -> movie_id, title, genres, description, year
    data/ratings.csv  -> user_id, movie_id, rating, timestamp
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Sci-Fi",
    "Thriller", "War", "Musical"
]

ADJECTIVES = [
    "Shadow", "Silent", "Broken", "Golden", "Last", "Hidden", "Eternal",
    "Crimson", "Lost", "Rising", "Frozen", "Midnight", "Secret", "Distant",
    "Ancient", "Burning", "Silver", "Forgotten", "Endless", "Wild"
]
NOUNS = [
    "Empire", "Horizon", "Legacy", "Journey", "Kingdom", "Storm", "City",
    "Dream", "War", "Star", "Garden", "River", "Prophecy", "Symphony",
    "Rebellion", "Voyage", "Mirror", "Labyrinth", "Harbor", "Echo"
]

DESCRIPTION_TEMPLATES = [
    "A gripping tale of {genre1} and {genre2} set against an unforgettable backdrop.",
    "When everything falls apart, a hero must rely on courage in this {genre1} story.",
    "A {genre1} {genre2} that blends heart-pounding moments with deep emotion.",
    "In a world on the edge, an unlikely alliance sparks a {genre1} adventure.",
    "A {genre2} that explores love, loss and redemption through a {genre1} lens.",
]


def generate_movies(n_movies=300):
    rows = []
    used_titles = set()
    for movie_id in range(1, n_movies + 1):
        # Unique title
        while True:
            title = f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)}"
            if title not in used_titles:
                used_titles.add(title)
                break

        n_genres = random.choice([1, 2, 2, 3])
        movie_genres = random.sample(GENRES, n_genres)
        genre1, genre2 = (movie_genres + movie_genres)[:2]
        description = random.choice(DESCRIPTION_TEMPLATES).format(
            genre1=genre1.lower(), genre2=genre2.lower()
        )
        year = random.randint(1980, 2025)

        rows.append({
            "movie_id": movie_id,
            "title": f"{title} ({year})",
            "genres": "|".join(movie_genres),
            "description": description,
            "year": year,
        })
    return pd.DataFrame(rows)


def generate_ratings(movies_df, n_users=250, min_ratings=15, max_ratings=80):
    """
    Simulate ratings with genre-based user taste so collaborative filtering
    has real signal to learn from (users who like similar genres rate
    similarly, rather than pure random noise).
    """
    rows = []
    start_date = datetime(2020, 1, 1)
    movie_ids = movies_df["movie_id"].tolist()
    genre_lookup = movies_df.set_index("movie_id")["genres"].to_dict()

    for user_id in range(1, n_users + 1):
        # Each user has 2-4 favorite genres that drive their ratings
        favorite_genres = set(random.sample(GENRES, random.randint(2, 4)))
        n_ratings = random.randint(min_ratings, max_ratings)
        rated_movies = random.sample(movie_ids, min(n_ratings, len(movie_ids)))

        for movie_id in rated_movies:
            movie_genres = set(genre_lookup[movie_id].split("|"))
            overlap = len(favorite_genres & movie_genres)

            # Base rating skewed by genre overlap with the user's taste
            base = 2.6 + overlap * 0.9
            noise = np.random.normal(0, 0.6)
            rating = np.clip(round((base + noise) * 2) / 2, 1.0, 5.0)  # nearest 0.5

            timestamp = start_date + timedelta(days=random.randint(0, 1500))
            rows.append({
                "user_id": user_id,
                "movie_id": movie_id,
                "rating": rating,
                "timestamp": timestamp.strftime("%Y-%m-%d"),
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    movies_df = generate_movies(n_movies=300)
    ratings_df = generate_ratings(movies_df, n_users=250)

    movies_df.to_csv("data/movies.csv", index=False)
    ratings_df.to_csv("data/ratings.csv", index=False)

    print(f"Generated {len(movies_df)} movies and {len(ratings_df)} ratings.")
    print("Saved to data/movies.csv and data/ratings.csv")

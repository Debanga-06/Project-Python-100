# 🎬 Movie Recommendation System

An advanced, fully working **Movie Recommendation System** built in pure Python, combining **Machine Learning algorithms** and **data processing** techniques. This project implements three classic recommendation strategies from scratch (using scikit-learn primitives) and demonstrates them end-to-end on a realistic synthetic dataset.

Built for: **Python 100 — Advanced Level Project**

---

## 📌 Features

| Algorithm | Technique | Solves |
|---|---|---|
| **Content-Based Filtering** | TF-IDF vectorization + Cosine Similarity | Cold-start for new users |
| **Collaborative Filtering (User-Based)** | Cosine similarity on user-item matrix | Taste-based neighbor recommendations |
| **Collaborative Filtering (Matrix Factorization)** | Truncated SVD (latent factors) | Sparse rating matrices, scalable prediction |
| **Hybrid Recommender** | Weighted blend of CB + CF scores | Filter-bubble & cold-start weaknesses of each single approach |

Also included:
- Synthetic but **realistic data generator** (300 movies, 250 users, ~12,000 ratings) with genre-driven user taste, so the models have real signal to learn from.
- **RMSE evaluation** of the collaborative filtering model using a train/test split.
- Clean, modular, object-oriented code — each algorithm is its own class in its own file.

---

## 🗂️ Project Structure

```
movie_recommendation_system/
├── data/
│   ├── generate_data.py     # Generates synthetic movies.csv & ratings.csv
│   ├── movies.csv           # Movie catalogue (id, title, genres, description, year)
│   └── ratings.csv          # User ratings (user_id, movie_id, rating, timestamp)
├── src/
│   ├── content_based.py         # ContentBasedRecommender (TF-IDF + cosine similarity)
│   ├── collaborative_filtering.py  # CollaborativeFilteringRecommender (SVD + user-based CF)
│   └── hybrid.py                # HybridRecommender (weighted blend)
├── main.py                  # Runs and demonstrates all three systems
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 1. Content-Based Filtering (`src/content_based.py`)
Each movie's **genres** and **description** are combined into a single text field and converted into a **TF-IDF (Term Frequency–Inverse Document Frequency)** vector. Movies are then compared using **cosine similarity** — the smaller the angle between two movie vectors, the more alike they are.

- `recommend(title)` → finds movies most similar to one seed movie.
- `recommend_for_profile(liked_titles)` → averages the TF-IDF vectors of several liked movies into a single "user profile" vector, then ranks the whole catalogue against it.

**Strength:** works instantly for brand-new users/movies with zero rating history.
**Weakness:** tends to recommend near-duplicates of what's already liked (filter bubble).

### 2. Collaborative Filtering (`src/collaborative_filtering.py`)
Built from the **user–item rating matrix** (rows = users, columns = movies, cells = ratings).

- **User-Based CF** (`recommend_user_based`): finds the *k* most similar users (cosine similarity on rating vectors) and recommends what they rated highly.
- **Matrix Factorization / SVD** (`recommend_svd`): decomposes the mean-centered rating matrix into latent factors with `TruncatedSVD`, then reconstructs the full matrix to predict ratings for *every* (user, movie) pair — including ones the user hasn't rated. This is the same family of technique used in the winning Netflix Prize solution.
- **`evaluate_rmse()`**: holds out 20% of ratings, retrains, and reports **Root Mean Squared Error** between predicted and true ratings, so you can quantify model accuracy.

**Strength:** discovers non-obvious recommendations based on collective behavior.
**Weakness:** struggles with brand-new users or movies that have few/no ratings (cold start).

### 3. Hybrid Recommender (`src/hybrid.py`)
Combines both signals into one score:

```
final_score = alpha * normalized(CF_score) + (1 - alpha) * normalized(CB_score)
```

`alpha` (default `0.6`) controls how much weight collaborative filtering gets vs. content similarity. This balances personalization (from CF) with relevance to explicitly liked movies (from CB), and still works reasonably even for users with limited history.

---

## 🧠 Machine Learning Concepts Used

- **TF-IDF vectorization** (`sklearn.feature_extraction.text.TfidfVectorizer`)
- **Cosine similarity** (`sklearn.metrics.pairwise.cosine_similarity`)
- **Dimensionality reduction / matrix factorization** (`sklearn.decomposition.TruncatedSVD`)
- **Train/test evaluation** (`sklearn.model_selection.train_test_split`, RMSE)
- **Data wrangling** with `pandas` (pivot tables, merges, group-bys)
- **Vectorized numeric computation** with `numpy`

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate the dataset (optional — `main.py` does this automatically if missing)
```bash
python data/generate_data.py
```

### 3. Run the system
```bash
python main.py
```

This will print, in order:
1. Content-based recommendations similar to a sample movie
2. SVD-based and user-based collaborative filtering recommendations for a sample user
3. RMSE evaluation of the collaborative model
4. Hybrid recommendations blending both approaches

---

## 📈 Example Output (abridged)

```
1. CONTENT-BASED FILTERING
Movies similar to: 'Golden Empire (1986)'
 movie_id             title                   genres        similarity_score
      218  Eternal Garden (1984)  Comedy|Musical|Animation             0.9123
       95  Broken Horizon (1981)                   Comedy             0.8832
...

2. COLLABORATIVE FILTERING
SVD (matrix factorization) recommendations for user 1:
 movie_id             title            genres        predicted_rating
       67  Wild Symphony (2007)  Sci-Fi|Thriller                  3.20
...
RMSE on held-out ratings: 0.80  (scale is 1-5 stars)

3. HYBRID RECOMMENDER (Content + Collaborative)
 movie_id                  title                 genres        hybrid_score
      233  Crimson Kingdom (2002)          Drama|Action              0.8164
...
```

---

## 🔧 Using It With Your Own Data

Replace `data/movies.csv` and `data/ratings.csv` with your own files, keeping the same columns:

- `movies.csv` → `movie_id, title, genres, description, year`
- `ratings.csv` → `user_id, movie_id, rating, timestamp`

Everything else (TF-IDF, SVD, hybrid blending, RMSE evaluation) works unchanged — for example, this schema is compatible with a trimmed-down version of the public **MovieLens** dataset.

---

## 📚 Possible Extensions (Great for a Viva / Project Report)

- Swap `TruncatedSVD` for `surprise`'s `SVD` (with bias terms) for better accuracy.
- Add implicit feedback (clicks/watch-time) alongside explicit star ratings.
- Serve recommendations through a **Flask/FastAPI** REST API.
- Add a **Streamlit** front-end for interactive exploration.
- Incorporate **deep learning** embeddings (Neural Collaborative Filtering) instead of SVD.

---

## 📄 License
This project is provided for educational purposes as part of a Python 100 advanced-level coursework submission.

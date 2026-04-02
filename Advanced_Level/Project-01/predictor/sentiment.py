"""
predictor/sentiment.py
News sentiment analysis using VADER + NewsAPI / yfinance news fallback.
"""

import pandas as pd
import numpy as np
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import Config


class SentimentAnalyzer:
    def __init__(self, cfg: Config):
        self.cfg      = cfg
        self.analyzer = SentimentIntensityAnalyzer()

    # ── Fetch News ────────────────────────────────────────────────
    def _fetch_newsapi(self) -> list[dict]:
        if not self.cfg.news_api_key:
            return []
        url = (
            "https://newsapi.org/v2/everything"
            f"?q={self.cfg.ticker}&language=en"
            f"&sortBy=publishedAt&pageSize={self.cfg.news_count}"
            f"&apiKey={self.cfg.news_api_key}"
        )
        try:
            r = requests.get(url, timeout=8)
            articles = r.json().get("articles", [])
            return [{"date": a["publishedAt"][:10],
                     "text": f"{a['title']} {a.get('description','')}"
                     } for a in articles]
        except Exception:
            return []

    def _fetch_yfinance_news(self) -> list[dict]:
        import yfinance as yf
        try:
            ticker   = yf.Ticker(self.cfg.ticker)
            news     = ticker.news or []
            results  = []
            for item in news[:self.cfg.news_count]:
                date = pd.to_datetime(item.get("providerPublishTime", 0), unit='s')
                text = item.get("title", "")
                results.append({"date": str(date.date()), "text": text})
            return results
        except Exception:
            return []

    # ── Score ─────────────────────────────────────────────────────
    def _score_article(self, text: str) -> float:
        return self.analyzer.polarity_scores(text)['compound']

    def _build_daily_sentiment(self, articles: list[dict]) -> pd.Series:
        if not articles:
            return pd.Series(dtype=float)
        records = []
        for a in articles:
            records.append({"date": pd.to_datetime(a["date"]),
                            "score": self._score_article(a["text"])})
        tmp = pd.DataFrame(records).set_index("date")
        daily = tmp['score'].resample('D').mean()
        return daily

    # ── Enrich DataFrame ──────────────────────────────────────────
    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        articles = self._fetch_newsapi() or self._fetch_yfinance_news()
        daily    = self._build_daily_sentiment(articles)

        if daily.empty:
            df['sentiment_score']    = 0.0
            df['sentiment_rolling']  = 0.0
            df['sentiment_positive'] = 0
            df['sentiment_negative'] = 0
            return df

        df['sentiment_score'] = df.index.map(
            lambda d: daily.get(pd.Timestamp(d), np.nan)
        )
        df['sentiment_score'].fillna(method='ffill', inplace=True)
        df['sentiment_score'].fillna(0, inplace=True)

        w = self.cfg.sentiment_window
        df['sentiment_rolling']  = df['sentiment_score'].rolling(w).mean().fillna(0)
        df['sentiment_positive'] = (df['sentiment_score'] > 0.05).astype(int)
        df['sentiment_negative'] = (df['sentiment_score'] < -0.05).astype(int)
        return df
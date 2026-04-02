"""
predictor/data_fetcher.py
Fetches OHLCV data from yfinance + Alpha Vantage fallback.
"""

import yfinance as yf
import pandas as pd
import requests
from config import Config


class DataFetcher:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    # ── Primary: yfinance ─────────────────────────────────────────
    def _fetch_yfinance(self) -> pd.DataFrame:
        ticker = yf.Ticker(self.cfg.ticker)
        df = ticker.history(period=self.cfg.period, interval=self.cfg.interval)
        df.index = pd.to_datetime(df.index).tz_localize(None)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        return df

    # ── Fallback: Alpha Vantage ───────────────────────────────────
    def _fetch_alpha_vantage(self) -> pd.DataFrame:
        url = (
            "https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY_ADJUSTED"
            f"&symbol={self.cfg.ticker}"
            f"&outputsize=full"
            f"&apikey={self.cfg.alpha_vantage_key}"
        )
        r    = requests.get(url, timeout=10)
        data = r.json().get("Time Series (Daily)", {})
        if not data:
            raise ValueError("Alpha Vantage returned no data.")

        rows = []
        for date, vals in data.items():
            rows.append({
                "Date":   date,
                "Open":   float(vals["1. open"]),
                "High":   float(vals["2. high"]),
                "Low":    float(vals["3. low"]),
                "Close":  float(vals["5. adjusted close"]),
                "Volume": int(vals["6. volume"]),
            })
        df = pd.DataFrame(rows)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date").sort_index()
        return df

    # ── Enrichments ───────────────────────────────────────────────
    def _add_fundamental_ratios(self, df: pd.DataFrame) -> pd.DataFrame:
        """Attach PE ratio & market cap as constant columns (latest snapshot)."""
        try:
            info = yf.Ticker(self.cfg.ticker).info
            df['pe_ratio']    = info.get('trailingPE',    0) or 0
            df['market_cap']  = info.get('marketCap',     0) or 0
            df['beta']        = info.get('beta',          1) or 1
            df['dividend_yield'] = info.get('dividendYield', 0) or 0
        except Exception:
            df['pe_ratio'] = df['market_cap'] = df['beta'] = df['dividend_yield'] = 0
        return df

    def _add_spy_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add SPY (S&P 500) as a market reference column."""
        try:
            spy = yf.Ticker("SPY").history(period=self.cfg.period, interval=self.cfg.interval)
            spy.index = pd.to_datetime(spy.index).tz_localize(None)
            spy = spy[['Close']].rename(columns={'Close': 'SPY_Close'})
            df  = df.join(spy, how='left')
            df['SPY_Close'].fillna(method='ffill', inplace=True)
        except Exception:
            df['SPY_Close'] = 0
        return df

    # ── Public API ────────────────────────────────────────────────
    def fetch(self) -> pd.DataFrame:
        try:
            df = self._fetch_yfinance()
        except Exception as e:
            print(f"   ⚠️  yfinance failed ({e}), trying Alpha Vantage...")
            df = self._fetch_alpha_vantage()

        df = df.dropna()
        df = self._add_fundamental_ratios(df)
        df = self._add_spy_correlation(df)

        # Daily return & log return
        df['daily_return']     = df['Close'].pct_change()
        df['log_return']       = (df['Close'] / df['Close'].shift(1)).apply(
                                    lambda x: x if pd.isna(x) else __import__('math').log(x))
        df['price_range']      = df['High'] - df['Low']
        df['gap']              = df['Open'] - df['Close'].shift(1)
        df = df.dropna()
        return df
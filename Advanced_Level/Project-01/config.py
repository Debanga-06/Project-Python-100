"""
config.py — Central configuration for Stock Price Predictor
"""

import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    # ── Stock & Data ──────────────────────────────────────────────
    ticker:        str  = "AAPL"
    period:        str  = "2y"          # yfinance period string
    interval:      str  = "1d"
    forecast_days: int  = 30

    # ── Model Hyperparameters ─────────────────────────────────────
    test_split:    float = 0.20         # 20 % held out for testing
    seq_len:       int   = 60           # LSTM look-back window
    lstm_epochs:   int   = 80
    lstm_units:    int   = 128
    lstm_dropout:  float = 0.2
    batch_size:    int   = 32

    rf_estimators: int   = 300
    xgb_estimators:int   = 300
    xgb_lr:        float = 0.05

    # ── Sentiment ─────────────────────────────────────────────────
    news_count:    int   = 20           # articles per fetch
    sentiment_window: int = 3           # rolling average window

    # ── Technical Indicator Windows ───────────────────────────────
    sma_windows:   List[int] = field(default_factory=lambda: [10, 20, 50, 200])
    ema_windows:   List[int] = field(default_factory=lambda: [12, 26])
    rsi_window:    int  = 14
    bb_window:     int  = 20
    macd_fast:     int  = 12
    macd_slow:     int  = 26
    macd_signal:   int  = 9
    atr_window:    int  = 14
    obv_enabled:   bool = True

    # ── Paths ─────────────────────────────────────────────────────
    output_dir:    str  = "output"
    report_dir:    str  = "reports"
    model_dir:     str  = "saved_models"

    # ── API Keys (set via environment variables) ──────────────────
    alpha_vantage_key: str = field(
        default_factory=lambda: os.getenv("ALPHA_VANTAGE_KEY", "demo")
    )
    news_api_key: str = field(
        default_factory=lambda: os.getenv("NEWS_API_KEY", "")
    )

    def __post_init__(self):
        for d in [self.output_dir, self.report_dir, self.model_dir,
                  f"{self.output_dir}/{self.ticker}"]:
            os.makedirs(d, exist_ok=True)

    @property
    def ticker_dir(self) -> str:
        return f"{self.output_dir}/{self.ticker}"
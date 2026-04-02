"""
predictor/feature_engineer.py
Builds 40+ technical indicators and lag features.
"""

import numpy as np
import pandas as pd
from config import Config


class FeatureEngineer:
    def __init__(self, cfg: Config):
        self.cfg          = cfg
        self.feature_cols = []          # populated after build()

    # ── Trend Indicators ──────────────────────────────────────────
    def _moving_averages(self, df):
        for w in self.cfg.sma_windows:
            df[f'SMA_{w}'] = df['Close'].rolling(w).mean()
        for w in self.cfg.ema_windows:
            df[f'EMA_{w}'] = df['Close'].ewm(span=w, adjust=False).mean()
        df['EMA_12_26_cross'] = df['EMA_12'] - df['EMA_26']
        return df

    def _macd(self, df):
        ema_fast   = df['Close'].ewm(span=self.cfg.macd_fast,   adjust=False).mean()
        ema_slow   = df['Close'].ewm(span=self.cfg.macd_slow,   adjust=False).mean()
        macd_line  = ema_fast - ema_slow
        signal     = macd_line.ewm(span=self.cfg.macd_signal,  adjust=False).mean()
        df['MACD']          = macd_line
        df['MACD_signal']   = signal
        df['MACD_hist']     = macd_line - signal
        return df

    # ── Momentum Indicators ───────────────────────────────────────
    def _rsi(self, df):
        delta = df['Close'].diff()
        gain  = delta.clip(lower=0).rolling(self.cfg.rsi_window).mean()
        loss  = (-delta.clip(upper=0)).rolling(self.cfg.rsi_window).mean()
        rs    = gain / (loss + 1e-10)
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    def _stochastic(self, df, k=14, d=3):
        low_min  = df['Low'].rolling(k).min()
        high_max = df['High'].rolling(k).max()
        df['Stoch_K'] = 100 * (df['Close'] - low_min) / (high_max - low_min + 1e-10)
        df['Stoch_D'] = df['Stoch_K'].rolling(d).mean()
        return df

    def _williams_r(self, df, period=14):
        high_max = df['High'].rolling(period).max()
        low_min  = df['Low'].rolling(period).min()
        df['Williams_R'] = -100 * (high_max - df['Close']) / (high_max - low_min + 1e-10)
        return df

    def _cci(self, df, period=20):
        tp  = (df['High'] + df['Low'] + df['Close']) / 3
        sma = tp.rolling(period).mean()
        mad = tp.rolling(period).apply(lambda x: np.abs(x - x.mean()).mean())
        df['CCI'] = (tp - sma) / (0.015 * mad + 1e-10)
        return df

    # ── Volatility Indicators ──────────────────────────────────────
    def _bollinger_bands(self, df):
        mid = df['Close'].rolling(self.cfg.bb_window).mean()
        std = df['Close'].rolling(self.cfg.bb_window).std()
        df['BB_upper']  = mid + 2 * std
        df['BB_lower']  = mid - 2 * std
        df['BB_mid']    = mid
        df['BB_width']  = (df['BB_upper'] - df['BB_lower']) / (mid + 1e-10)
        df['BB_pct']    = (df['Close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower'] + 1e-10)
        return df

    def _atr(self, df):
        tr = pd.concat([
            df['High'] - df['Low'],
            (df['High'] - df['Close'].shift()).abs(),
            (df['Low']  - df['Close'].shift()).abs()
        ], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(self.cfg.atr_window).mean()
        return df

    def _historical_volatility(self, df, window=21):
        df['HV_21'] = df['log_return'].rolling(window).std() * np.sqrt(252)
        return df

    # ── Volume Indicators ──────────────────────────────────────────
    def _obv(self, df):
        direction    = np.sign(df['Close'].diff())
        df['OBV']    = (direction * df['Volume']).cumsum()
        df['OBV_EMA']= df['OBV'].ewm(span=20, adjust=False).mean()
        return df

    def _vwap(self, df):
        tp           = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP']   = (tp * df['Volume']).cumsum() / df['Volume'].cumsum()
        return df

    def _mfi(self, df, period=14):
        tp  = (df['High'] + df['Low'] + df['Close']) / 3
        rmf = tp * df['Volume']
        pos = rmf.where(tp > tp.shift(1), 0).rolling(period).sum()
        neg = rmf.where(tp < tp.shift(1), 0).rolling(period).sum()
        df['MFI'] = 100 - (100 / (1 + pos / (neg + 1e-10)))
        return df

    # ── Lag & Rolling Stats ────────────────────────────────────────
    def _lag_features(self, df, lags=[1, 2, 3, 5, 10, 20]):
        for lag in lags:
            df[f'Close_lag_{lag}']  = df['Close'].shift(lag)
            df[f'Return_lag_{lag}'] = df['daily_return'].shift(lag)
        return df

    def _rolling_stats(self, df, windows=[5, 10, 20]):
        for w in windows:
            df[f'rolling_mean_{w}'] = df['Close'].rolling(w).mean()
            df[f'rolling_std_{w}']  = df['Close'].rolling(w).std()
            df[f'rolling_min_{w}']  = df['Close'].rolling(w).min()
            df[f'rolling_max_{w}']  = df['Close'].rolling(w).max()
            df[f'rolling_skew_{w}'] = df['daily_return'].rolling(w).skew()
        return df

    # ── Calendar Features ─────────────────────────────────────────
    def _calendar_features(self, df):
        df['day_of_week']  = df.index.dayofweek
        df['month']        = df.index.month
        df['quarter']      = df.index.quarter
        df['is_month_end'] = df.index.is_month_end.astype(int)
        df['is_month_start']= df.index.is_month_start.astype(int)
        return df

    # ── Target ────────────────────────────────────────────────────
    def _add_target(self, df):
        df['Target'] = df['Close'].shift(-1)   # next-day close price
        return df

    # ── Public API ────────────────────────────────────────────────
    def build(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._moving_averages(df)
        df = self._macd(df)
        df = self._rsi(df)
        df = self._stochastic(df)
        df = self._williams_r(df)
        df = self._cci(df)
        df = self._bollinger_bands(df)
        df = self._atr(df)
        df = self._historical_volatility(df)
        df = self._obv(df)
        df = self._vwap(df)
        df = self._mfi(df)
        df = self._lag_features(df)
        df = self._rolling_stats(df)
        df = self._calendar_features(df)
        df = self._add_target(df)
        df = df.dropna()

        exclude = {'Open', 'High', 'Low', 'Close', 'Volume',
                   'Target', 'daily_return', 'log_return',
                   'SPY_Close', 'price_range', 'gap'}
        self.feature_cols = [c for c in df.columns if c not in exclude]
        return df

    # ── Helpers for forecast ──────────────────────────────────────
    def build_forecast_row(self, df: pd.DataFrame) -> pd.DataFrame:
        """Re-run build on extended df to get next feature row."""
        return self.build(df.copy())
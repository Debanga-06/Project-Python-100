"""
predictor/visualizer.py
Generates publication-quality charts using Matplotlib & Plotly.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import Config

DARK_BG  = '#0d1117'
GRID_CLR = '#21262d'
TEXT_CLR = '#c9d1d9'
GREEN    = '#3fb950'
RED      = '#f85149'
BLUE     = '#58a6ff'
ORANGE   = '#d29922'
PURPLE   = '#bc8cff'


class Visualizer:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        plt.style.use('dark_background')

    def _save(self, fig, name):
        path = os.path.join(self.cfg.ticker_dir, name)
        fig.savefig(path, dpi=150, bbox_inches='tight',
                    facecolor=DARK_BG, edgecolor='none')
        plt.close(fig)
        return path

    # ── 1. Price + Technical Overview ─────────────────────────────
    def plot_technical(self, df: pd.DataFrame):
        fig = plt.figure(figsize=(18, 14), facecolor=DARK_BG)
        gs  = gridspec.GridSpec(4, 1, figure=fig, hspace=0.08,
                                height_ratios=[3, 1, 1, 1])

        ax1 = fig.add_subplot(gs[0])   # Price + BB + MAs
        ax2 = fig.add_subplot(gs[1], sharex=ax1)  # Volume
        ax3 = fig.add_subplot(gs[2], sharex=ax1)  # RSI
        ax4 = fig.add_subplot(gs[3], sharex=ax1)  # MACD

        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor(DARK_BG)
            ax.tick_params(colors=TEXT_CLR)
            ax.yaxis.label.set_color(TEXT_CLR)
            ax.spines[:].set_color(GRID_CLR)

        # Candlestick (simplified as OHLC fill)
        up   = df[df['Close'] >= df['Open']]
        down = df[df['Close'] <  df['Open']]
        ax1.bar(up.index,   up['Close']  - up['Open'],   bottom=up['Open'],   color=GREEN,  width=0.6, alpha=0.8)
        ax1.bar(down.index, down['Close']- down['Open'], bottom=down['Open'], color=RED,    width=0.6, alpha=0.8)
        ax1.bar(df.index,   df['High']   - df['Low'],    bottom=df['Low'],    color=TEXT_CLR, width=0.1, alpha=0.3)

        # Bollinger Bands
        ax1.fill_between(df.index, df['BB_upper'], df['BB_lower'],
                         alpha=0.08, color=BLUE, label='Bollinger Bands')
        ax1.plot(df.index, df['BB_upper'], color=BLUE,   linewidth=0.5, alpha=0.5)
        ax1.plot(df.index, df['BB_lower'], color=BLUE,   linewidth=0.5, alpha=0.5)
        ax1.plot(df.index, df['SMA_20'],   color=ORANGE, linewidth=1.2, label='SMA 20', alpha=0.9)
        ax1.plot(df.index, df['SMA_50'],   color=PURPLE, linewidth=1.2, label='SMA 50', alpha=0.9)
        ax1.set_title(f"{self.cfg.ticker} — Technical Analysis",
                      color=TEXT_CLR, fontsize=16, pad=12, fontweight='bold')
        ax1.legend(facecolor=DARK_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR, fontsize=9)
        ax1.set_ylabel('Price ($)', color=TEXT_CLR)

        # Volume
        ax2.bar(up.index,   up['Volume'],   color=GREEN, alpha=0.7)
        ax2.bar(down.index, down['Volume'], color=RED,   alpha=0.7)
        ax2.set_ylabel('Volume', color=TEXT_CLR)

        # RSI
        ax3.plot(df.index, df['RSI'], color=ORANGE, linewidth=1.2)
        ax3.axhline(70, color=RED,   linestyle='--', linewidth=0.8, alpha=0.7)
        ax3.axhline(30, color=GREEN, linestyle='--', linewidth=0.8, alpha=0.7)
        ax3.fill_between(df.index, 70, df['RSI'], where=df['RSI']>70, color=RED,   alpha=0.15)
        ax3.fill_between(df.index, 30, df['RSI'], where=df['RSI']<30, color=GREEN, alpha=0.15)
        ax3.set_ylim(0, 100)
        ax3.set_ylabel('RSI', color=TEXT_CLR)

        # MACD
        colors = [GREEN if v >= 0 else RED for v in df['MACD_hist']]
        ax4.bar(df.index, df['MACD_hist'], color=colors, alpha=0.7)
        ax4.plot(df.index, df['MACD'],        color=BLUE,   linewidth=1.0, label='MACD')
        ax4.plot(df.index, df['MACD_signal'], color=ORANGE, linewidth=1.0, label='Signal')
        ax4.axhline(0, color=GRID_CLR, linewidth=0.8)
        ax4.set_ylabel('MACD', color=TEXT_CLR)
        ax4.legend(facecolor=DARK_BG, edgecolor=GRID_CLR, labelcolor=TEXT_CLR, fontsize=9)
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)

        self._save(fig, 'technical_analysis.png')

    # ── 2. Model Performance ───────────────────────────────────────
    def plot_model_performance(self, df, results):
        n   = len(results)
        fig, axes = plt.subplots(n, 1, figsize=(16, 5 * n), facecolor=DARK_BG)
        if n == 1:
            axes = [axes]

        colors_map = {'RandomForest': GREEN, 'XGBoost': ORANGE, 'LSTM': PURPLE}

        for ax, (name, metrics) in zip(axes, results.items()):
            ax.set_facecolor(DARK_BG)
            ax.spines[:].set_color(GRID_CLR)
            ax.tick_params(colors=TEXT_CLR)

            actual = metrics['actual']
            preds  = metrics['preds']
            x      = range(len(actual))

            ax.plot(x, actual, color=BLUE,                 linewidth=1.2, label='Actual', alpha=0.9)
            ax.plot(x, preds,  color=colors_map.get(name, WHITE), linewidth=1.2,
                    label=f'{name} Prediction', alpha=0.9, linestyle='--')
            ax.fill_between(x, actual, preds,
                            where=np.array(preds) > np.array(actual),
                            alpha=0.08, color=RED)
            ax.fill_between(x, actual, preds,
                            where=np.array(preds) <= np.array(actual),
                            alpha=0.08, color=GREEN)

            ax.set_title(
                f"{name}  |  RMSE: {metrics['rmse']:.4f}  "
                f"MAE: {metrics['mae']:.4f}  R²: {metrics['r2']:.4f}  "
                f"MAPE: {metrics['mape']:.2f}%",
                color=TEXT_CLR, fontsize=12, fontweight='bold')
            ax.set_ylabel('Price ($)', color=TEXT_CLR)
            ax.legend(facecolor=DARK_BG, edgecolor=GRID_CLR,
                      labelcolor=TEXT_CLR, fontsize=9)

        fig.suptitle(f"{self.cfg.ticker} — Model Performance Comparison",
                     color=TEXT_CLR, fontsize=16, fontweight='bold', y=1.01)
        self._save(fig, 'model_performance.png')

    # ── 3. Forecast Chart ──────────────────────────────────────────
    def plot_forecast(self, df, forecast_df):
        fig, ax = plt.subplots(figsize=(16, 8), facecolor=DARK_BG)
        ax.set_facecolor(DARK_BG)
        ax.spines[:].set_color(GRID_CLR)
        ax.tick_params(colors=TEXT_CLR)

        hist = df['Close'].iloc[-120:]
        ax.plot(hist.index, hist.values, color=BLUE, linewidth=1.5, label='Historical')

        # Forecast band
        cols = [c for c in forecast_df.columns if c != 'ensemble']
        if len(cols) > 1:
            hi = forecast_df[cols].max(axis=1)
            lo = forecast_df[cols].min(axis=1)
            ax.fill_between(forecast_df.index, lo, hi,
                            alpha=0.15, color=ORANGE, label='Model Range')

        ax.plot(forecast_df.index, forecast_df['ensemble'],
                color=ORANGE, linewidth=2.0, label='Ensemble Forecast',
                linestyle='--', marker='o', markersize=4)

        # Vertical divider
        ax.axvline(df.index[-1], color=GRID_CLR, linestyle=':', linewidth=1.0)
        ax.text(df.index[-1], ax.get_ylim()[0],
                ' Forecast →', color=TEXT_CLR, fontsize=9, alpha=0.7)

        last_price = df['Close'].iloc[-1]
        pred_price = forecast_df['ensemble'].iloc[-1]
        change_pct = (pred_price - last_price) / last_price * 100
        color_chg  = GREEN if change_pct > 0 else RED

        ax.set_title(
            f"{self.cfg.ticker} — {len(forecast_df)}-Day Price Forecast  "
            f"| {change_pct:+.2f}%",
            color=color_chg, fontsize=15, fontweight='bold')
        ax.set_ylabel('Price ($)', color=TEXT_CLR)
        ax.legend(facecolor=DARK_BG, edgecolor=GRID_CLR,
                  labelcolor=TEXT_CLR, fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

        self._save(fig, 'forecast.png')

    # ── 4. Feature Importance ─────────────────────────────────────
    def plot_feature_importance(self, models, feature_cols):
        fig, axes = plt.subplots(1, 2, figsize=(18, 8), facecolor=DARK_BG)
        names_map = {'RandomForest': GREEN, 'XGBoost': ORANGE}

        for ax, (name, color) in zip(axes, names_map.items()):
            if name not in models:
                continue
            m = models[name]
            imp = pd.Series(m.feature_importances_, index=feature_cols).nlargest(20)
            ax.set_facecolor(DARK_BG)
            ax.spines[:].set_color(GRID_CLR)
            ax.tick_params(colors=TEXT_CLR)
            ax.barh(imp.index[::-1], imp.values[::-1], color=color, alpha=0.85)
            ax.set_title(f"{name} — Top 20 Features",
                         color=TEXT_CLR, fontsize=13, fontweight='bold')
            ax.set_xlabel('Importance', color=TEXT_CLR)

        self._save(fig, 'feature_importance.png')

    # ── 5. Interactive Plotly Chart ────────────────────────────────
    def plot_interactive(self, df, forecast_df):
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                            row_heights=[0.6, 0.2, 0.2],
                            subplot_titles=('Price & Forecast', 'Volume', 'RSI'))

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='OHLC',
            increasing_line_color=GREEN, decreasing_line_color=RED
        ), row=1, col=1)

        # SMA
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'],
            name='SMA 20', line=dict(color=ORANGE, width=1)), row=1, col=1)

        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_df.index, y=forecast_df['ensemble'],
            name='Forecast', line=dict(color=PURPLE, width=2, dash='dash'),
            mode='lines+markers'
        ), row=1, col=1)

        # Volume
        colors = [GREEN if c >= o else RED
                  for c, o in zip(df['Close'], df['Open'])]
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'],
            name='Volume', marker_color=colors, opacity=0.7), row=2, col=1)

        # RSI
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'],
            name='RSI', line=dict(color=ORANGE, width=1)), row=3, col=1)
        fig.add_hline(y=70, line_dash='dash', line_color=RED,   row=3, col=1)
        fig.add_hline(y=30, line_dash='dash', line_color=GREEN, row=3, col=1)

        fig.update_layout(
            template='plotly_dark',
            title=f"{self.cfg.ticker} — Interactive Analysis & Forecast",
            xaxis_rangeslider_visible=False,
            height=900,
            paper_bgcolor=DARK_BG,
            plot_bgcolor=DARK_BG
        )

        path = os.path.join(self.cfg.ticker_dir, 'interactive.html')
        fig.write_html(path)

    # ── Main Entry ─────────────────────────────────────────────────
    def plot_all(self, df, forecast_df, results):
        self.plot_technical(df)
        self.plot_model_performance(df, results)
        self.plot_forecast(df, forecast_df)
        self.plot_interactive(df, forecast_df)
        if results:
            from predictor.models import ModelEnsemble
        print(f"   ✅ Charts saved to output/{self.cfg.ticker}/")
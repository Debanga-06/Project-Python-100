"""
╔══════════════════════════════════════════════════════════════════╗
║           STOCK PRICE PREDICTOR - Advanced ML System            ║
║     Using LSTM, Random Forest, XGBoost & Sentiment Analysis     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import warnings
warnings.filterwarnings('ignore')

from predictor.data_fetcher import DataFetcher
from predictor.feature_engineer import FeatureEngineer
from predictor.models import ModelEnsemble
from predictor.sentiment import SentimentAnalyzer
from predictor.visualizer import Visualizer
from predictor.report import ReportGenerator
from config import Config
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Advanced Stock Price Predictor")
    parser.add_argument("--ticker",   type=str, default="AAPL",  help="Stock ticker symbol")
    parser.add_argument("--period",   type=str, default="2y",    help="Data period (1y, 2y, 5y)")
    parser.add_argument("--days",     type=int, default=30,      help="Days to predict ahead")
    parser.add_argument("--models",   type=str, default="all",   help="Models: all | lstm | rf | xgb")
    parser.add_argument("--report",   action="store_true",       help="Generate HTML report")
    return parser.parse_args()


def main():
    args = parse_args()
    cfg  = Config(ticker=args.ticker, period=args.period, forecast_days=args.days)

    print(f"\n{'='*65}")
    print(f"  📈 Stock Price Predictor — {args.ticker.upper()}")
    print(f"  Period: {args.period}  |  Forecast: {args.days} days ahead")
    print(f"{'='*65}\n")

    # ── 1. Fetch Data ──────────────────────────────────────────────
    print("🔄 [1/6] Fetching market data via API...")
    fetcher = DataFetcher(cfg)
    df      = fetcher.fetch()
    print(f"   ✅ Loaded {len(df)} trading days for {args.ticker}\n")

    # ── 2. Sentiment Analysis ──────────────────────────────────────
    print("🔄 [2/6] Analysing news sentiment...")
    sentiment = SentimentAnalyzer(cfg)
    df        = sentiment.enrich(df)
    score     = df['sentiment_score'].mean()
    label     = "🟢 Positive" if score > 0 else ("🔴 Negative" if score < 0 else "🟡 Neutral")
    print(f"   ✅ Overall sentiment: {label} ({score:.3f})\n")

    # ── 3. Feature Engineering ─────────────────────────────────────
    print("🔄 [3/6] Engineering technical indicators & features...")
    engineer = FeatureEngineer(cfg)
    df       = engineer.build(df)
    print(f"   ✅ Generated {len(engineer.feature_cols)} features\n")

    # ── 4. Train Models ────────────────────────────────────────────
    print("🔄 [4/6] Training ML ensemble...")
    ensemble = ModelEnsemble(cfg, args.models)
    results  = ensemble.fit_evaluate(df, engineer.feature_cols)

    for name, metrics in results.items():
        print(f"   📊 {name:<20} RMSE={metrics['rmse']:.4f}  MAE={metrics['mae']:.4f}  R²={metrics['r2']:.4f}")
    print()

    # ── 5. Forecast ────────────────────────────────────────────────
    print("🔄 [5/6] Generating forecast...")
    forecast_df = ensemble.forecast(df, engineer, args.days)
    last_price  = df['Close'].iloc[-1]
    pred_price  = forecast_df['ensemble'].iloc[-1]
    change_pct  = ((pred_price - last_price) / last_price) * 100
    direction   = "📈 BULLISH" if change_pct > 0 else "📉 BEARISH"

    print(f"\n   {'─'*45}")
    print(f"   Current Price : ${last_price:.2f}")
    print(f"   {args.days}-Day Forecast : ${pred_price:.2f}  ({change_pct:+.2f}%)")
    print(f"   Signal        : {direction}")
    print(f"   {'─'*45}\n")

    # ── 6. Visualise & Report ──────────────────────────────────────
    print("🔄 [6/6] Generating charts & report...")
    viz = Visualizer(cfg)
    viz.plot_all(df, forecast_df, results)

    if args.report:
        rpt = ReportGenerator(cfg)
        rpt.generate(df, forecast_df, results, score)
        print(f"   ✅ Report saved → reports/{args.ticker}_report.html\n")

    print(f"{'='*65}")
    print(f"  ✅ All done! Charts saved to → output/{args.ticker}/")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
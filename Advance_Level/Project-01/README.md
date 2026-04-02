# 📈 Stock Price Predictor

> Advanced ML system using LSTM · Random Forest · XGBoost · Sentiment Analysis

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13%2B-FF6F00?style=flat-square&logo=tensorflow)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0%2B-189fdd?style=flat-square)

---

## 🚀 Features

- **Multi-model Ensemble** — Bidirectional LSTM + Random Forest + XGBoost
- **40+ Technical Indicators** — RSI, MACD, Bollinger Bands, ATR, OBV, VWAP, Stochastic, CCI, Williams %R, and more
- **Sentiment Analysis** — VADER NLP on live news via NewsAPI + yfinance fallback
- **Live Data** — yfinance primary, Alpha Vantage fallback
- **Interactive Charts** — Matplotlib dark-theme + Plotly HTML dashboard
- **HTML Report** — Self-contained report with embedded charts
- **Model Persistence** — Saves trained models to disk for reuse

---

## 📁 Project Structure

```
stock_predictor/
├── main.py                    # Entry point
├── config.py                  # Central configuration
├── requirements.txt
├── predictor/
│   ├── data_fetcher.py        # yfinance + Alpha Vantage API
│   ├── feature_engineer.py    # 40+ technical indicators
│   ├── models.py              # LSTM + RF + XGBoost ensemble
│   ├── sentiment.py           # VADER news sentiment
│   ├── visualizer.py          # Matplotlib + Plotly charts
│   └── report.py              # HTML report generator
├── output/                    # Charts saved here
├── reports/                   # HTML reports saved here
└── saved_models/              # Trained model files
```

---

## ⚙️ Setup

```bash
# 1. Clone / download the project
cd stock_predictor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set API keys in environment
export NEWS_API_KEY="your_key_here"          # https://newsapi.org
export ALPHA_VANTAGE_KEY="your_key_here"     # https://www.alphavantage.co
```

---

## ▶️ Usage

```bash
# Basic — predict AAPL for next 30 days
python main.py --ticker AAPL

# Custom ticker, period, forecast window
python main.py --ticker TSLA --period 5y --days 60

# Use only specific models
python main.py --ticker MSFT --models lstm
python main.py --ticker GOOGL --models rf,xgb

# Generate full HTML report
python main.py --ticker NVDA --report
```

### Arguments

| Argument  | Default | Description                          |
|-----------|---------|--------------------------------------|
| `--ticker`| AAPL    | Stock ticker symbol                  |
| `--period`| 2y      | Historical data period (1y/2y/5y)    |
| `--days`  | 30      | Days to forecast ahead               |
| `--models`| all     | Models to use: all / lstm / rf / xgb |
| `--report`| False   | Generate HTML report                 |

---

## 📊 Output Files

```
output/AAPL/
├── technical_analysis.png     # Candlestick + BB + RSI + MACD
├── model_performance.png      # Actual vs predicted per model
├── forecast.png               # Future price forecast chart
└── interactive.html           # Full Plotly interactive dashboard

reports/
└── AAPL_report.html           # Self-contained analysis report
```

---

## ⚠️ Disclaimer

> This project is for **educational purposes only**.  
> It is **not financial advice**. Never invest based on ML model predictions alone.

---

## 📄 License

GNU Affero General Public License v3.0 — see [LICENSE](LICENSE)
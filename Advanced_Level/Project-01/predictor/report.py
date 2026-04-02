"""
predictor/report.py
Generates a self-contained HTML report with embedded charts.
"""

import os
import base64
from datetime import datetime
from config import Config


def _img_to_b64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


class ReportGenerator:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def generate(self, df, forecast_df, results, sentiment_score):
        ticker    = self.cfg.ticker
        now       = datetime.now().strftime("%Y-%m-%d %H:%M")
        last_px   = df['Close'].iloc[-1]
        pred_px   = forecast_df['ensemble'].iloc[-1]
        change    = (pred_px - last_px) / last_px * 100
        direction = "BULLISH 📈" if change > 0 else "BEARISH 📉"
        sent_lbl  = ("Positive 🟢" if sentiment_score > 0
                     else ("Negative 🔴" if sentiment_score < 0 else "Neutral 🟡"))

        td     = self.cfg.ticker_dir
        charts = {
            "Technical Analysis":      _img_to_b64(f"{td}/technical_analysis.png"),
            "Model Performance":       _img_to_b64(f"{td}/model_performance.png"),
            "Price Forecast":          _img_to_b64(f"{td}/forecast.png"),
        }

        rows = ""
        for name, m in results.items():
            rows += f"""
            <tr>
                <td>{name}</td>
                <td>{m['rmse']:.4f}</td>
                <td>{m['mae']:.4f}</td>
                <td>{m['r2']:.4f}</td>
                <td>{m['mape']:.2f}%</td>
            </tr>"""

        chart_html = ""
        for title, b64 in charts.items():
            if b64:
                chart_html += f"""
                <div class="chart-block">
                    <h3>{title}</h3>
                    <img src="data:image/png;base64,{b64}" alt="{title}" />
                </div>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{ticker} Stock Analysis Report</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0d1117; color:#c9d1d9; font-family:'Segoe UI',sans-serif; padding:2rem; }}
  h1   {{ color:#58a6ff; font-size:2rem; margin-bottom:.5rem; }}
  h2   {{ color:#58a6ff; margin:2rem 0 1rem; border-bottom:1px solid #21262d; padding-bottom:.5rem; }}
  h3   {{ color:#c9d1d9; margin:1.5rem 0 .5rem; }}
  .meta {{ color:#8b949e; font-size:.9rem; margin-bottom:2rem; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1rem; margin:1.5rem 0; }}
  .kpi {{ background:#161b22; border:1px solid #21262d; border-radius:10px; padding:1.2rem; text-align:center; }}
  .kpi .val {{ font-size:1.8rem; font-weight:bold; color:#58a6ff; }}
  .kpi .lbl {{ font-size:.8rem; color:#8b949e; margin-top:.3rem; }}
  .bull {{ color:#3fb950 !important; }}
  .bear {{ color:#f85149 !important; }}
  table {{ width:100%; border-collapse:collapse; margin:1rem 0; }}
  th,td {{ padding:.75rem 1rem; text-align:left; border-bottom:1px solid #21262d; }}
  th {{ background:#161b22; color:#58a6ff; }}
  tr:hover {{ background:#161b22; }}
  .chart-block {{ margin:2rem 0; }}
  .chart-block img {{ width:100%; border-radius:10px; border:1px solid #21262d; }}
  footer {{ margin-top:3rem; color:#8b949e; font-size:.8rem; text-align:center; }}
</style>
</head>
<body>

<h1>📈 {ticker} — Stock Analysis Report</h1>
<p class="meta">Generated: {now} &nbsp;|&nbsp; Period: {self.cfg.period} &nbsp;|&nbsp; Forecast: {self.cfg.forecast_days} days</p>

<h2>📊 Key Metrics</h2>
<div class="kpi-grid">
  <div class="kpi"><div class="val">${last_px:.2f}</div><div class="lbl">Current Price</div></div>
  <div class="kpi"><div class="val {'bull' if change>0 else 'bear'}">${pred_px:.2f}</div><div class="lbl">{self.cfg.forecast_days}-Day Forecast</div></div>
  <div class="kpi"><div class="val {'bull' if change>0 else 'bear'}">{change:+.2f}%</div><div class="lbl">Expected Change</div></div>
  <div class="kpi"><div class="val">{direction}</div><div class="lbl">Signal</div></div>
  <div class="kpi"><div class="val">{sent_lbl}</div><div class="lbl">News Sentiment</div></div>
  <div class="kpi"><div class="val">{df['RSI'].iloc[-1]:.1f}</div><div class="lbl">RSI (Current)</div></div>
</div>

<h2>🤖 Model Performance</h2>
<table>
  <thead><tr><th>Model</th><th>RMSE</th><th>MAE</th><th>R²</th><th>MAPE</th></tr></thead>
  <tbody>{rows}</tbody>
</table>

<h2>📉 Charts</h2>
{chart_html}

<footer>
  Stock Price Predictor &nbsp;|&nbsp; For educational purposes only. Not financial advice.
</footer>
</body>
</html>"""

        path = os.path.join(self.cfg.report_dir, f"{ticker}_report.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path
from flask import Flask, request, jsonify, send_file
import numpy as np
import pandas as pd
import yfinance as yf
from model import train_and_predict, evaluate_backtest
from features import add_features

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/style.css")
def css():
    return send_file("style.css")

@app.route("/app.js")
def js():
    return send_file("app.js")

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True) or {}
    ticker = (payload.get("ticker") or "").strip().upper()

    if not ticker:
        return jsonify({"error": "Ticker is required (example: AAPL)"}), 400

    df = yf.download(ticker, period="1y", auto_adjust=True)

    if df.empty:
        return jsonify({"error": f"No data found for ticker: {ticker}"}), 404

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    close_series = df["Close"]
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]

    feature_df = add_features(df.copy())
    prices = close_series.dropna().to_numpy(dtype=float)

    if len(prices) < 15:
        return jsonify({"error": "Not enough data to build prediction."}), 400

    preds = train_and_predict(prices)
    backtest = evaluate_backtest(prices)
    last_30 = prices[-30:]
    projected = np.array(preds, dtype=float)

    trend_pct = float(((projected[-1] - last_30[-1]) / last_30[-1]) * 100)
    avg_return = np.diff(last_30) / last_30[:-1]
    volatility_pct = float(np.std(avg_return) * 100)

    latest = feature_df.iloc[-1]

    return jsonify({
        "ticker": ticker,
        "history": [float(v) for v in last_30.tolist()],
        "predictions": preds,
        "metrics": {
            "latest_close": float(last_30[-1]),
            "predicted_close_5d": float(projected[-1]),
            "trend_5d_pct": trend_pct,
            "volatility_30d_pct": volatility_pct,
            "ma10": float(latest["MA10"]),
            "ma50": float(latest["MA50"]),
            "rsi": float(latest["RSI"]),
            "backtest_mae": backtest["mae"],
            "backtest_mape": backtest["mape"],
            "backtest_samples": backtest["samples"],
        },
    })

if __name__ == "__main__":
    app.run(debug=True)
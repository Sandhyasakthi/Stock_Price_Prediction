import numpy as np
import yfinance as yf

from model import prepare_data
from sklearn.ensemble import RandomForestRegressor


def evaluate_ticker(ticker: str = "AAPL"):
    df = yf.download(ticker, period="1y")
    prices = df["Close"].dropna().values

    X, y = prepare_data(prices, window=5)
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = float(np.mean(np.abs(y_test - preds)))
    mape = float(np.mean(np.abs((y_test - preds) / y_test)) * 100)

    print(f"Ticker: {ticker}")
    print(f"Samples (train/test): {len(X_train)}/{len(X_test)}")
    print(f"MAE: {mae:.4f}")
    print(f"MAPE: {mape:.2f}%")


if __name__ == "__main__":
    evaluate_ticker("AAPL")

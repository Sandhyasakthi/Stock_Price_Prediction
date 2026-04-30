import numpy as np
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=200, random_state=42)

def prepare_data(data, window=5):
    X, y = [], []
    for i in range(window, len(data)):
        X.append(data[i-window:i])
        y.append(data[i])
    return np.array(X), np.array(y)

def train_and_predict(data):
    X, y = prepare_data(data)

    if len(X) == 0:
        return []

    model.fit(X, y)

    last_window = data[-5:]
    preds = []

    for _ in range(5):  # predict next 5 days
        pred = model.predict([last_window])[0]
        preds.append(float(pred))

        last_window = np.append(last_window[1:], pred)

    return preds


def evaluate_backtest(data, window=5, train_ratio=0.8):
    X, y = prepare_data(data, window=window)
    if len(X) < 20:
        return {"mae": None, "mape": None, "samples": 0}

    split = int(len(X) * train_ratio)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    if len(X_test) == 0:
        return {"mae": None, "mape": None, "samples": 0}

    eval_model = RandomForestRegressor(n_estimators=200, random_state=42)
    eval_model.fit(X_train, y_train)
    preds = eval_model.predict(X_test)

    mae = float(np.mean(np.abs(y_test - preds)))
    safe_denominator = np.where(y_test == 0, np.nan, y_test)
    mape = float(np.nanmean(np.abs((y_test - preds) / safe_denominator)) * 100)

    return {"mae": mae, "mape": mape, "samples": int(len(X_test))}
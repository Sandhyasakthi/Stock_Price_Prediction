# Long-Term Stock Price Forecasting Dashboard

A full-stack machine learning dashboard that forecasts the next 5 closing prices for a stock ticker using live Yahoo Finance data, then visualizes predictions and technical indicators in an interactive pastel-themed UI.

---

## Project Overview

This project is designed as a mini fintech analytics product, not just a notebook model.  
It combines:

- real-time market data ingestion
- feature engineering with technical indicators
- ML-based short-term forecasting
- backend analytics API
- responsive frontend dashboard for end users

---

## Key Features

- **Live Data Fetching** from Yahoo Finance via `yfinance`
- **5-Day Price Forecasting** using `RandomForestRegressor`
- **Technical Indicators**: MA10, MA50, RSI
- **Risk/Trend Metrics**: 5-day trend %, 30-day volatility %
- **Model Evaluation Signal**: backtest-style MAE/MAPE support
- **Interactive Dashboard UI** with KPI cards, chart, and forecast table
- **Input Validation & Error Handling** for invalid/empty tickers

---

## Tech Stack

- **Backend**: Python, Flask
- **ML/Data**: NumPy, Pandas, scikit-learn, yfinance
- **Frontend**: HTML, CSS, JavaScript, Chart.js

---

## Project Structure

```text
.
├── app.py            # Flask app + REST API endpoints
├── model.py          # Forecasting + evaluation logic
├── features.py       # Technical indicator calculations
├── train.py          # Offline model evaluation script
├── index.html        # Dashboard layout
├── style.css         # Pastel theme styling
├── app.js            # Frontend API integration + chart rendering
├── requirements.txt  # Python dependencies
└── README.md
```

---

## How It Works

1. User enters a ticker (example: `AAPL` or `RELIANCE.NS`)
2. Frontend sends POST request to `/predict`
3. Backend downloads 1-year historical close prices
4. Features (MA10, MA50, RSI) are computed
5. Model predicts next 5 closing prices
6. API returns:
   - recent history
   - forecast values
   - analytics metrics
7. Dashboard renders cards, chart, and forecast table

---

## Installation & Run

### 1) Clone repository

```bash
git clone <your-repo-url>
cd "Long-Term Stock Price Forecasting"
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the app

```bash
python app.py
```

Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Usage

- Enter ticker symbol in input box
- Click **Analyze**
- View:
  - latest close and predicted close
  - trend and volatility
  - MA10/MA50 and RSI
  - historical vs forecast line chart
  - day-wise 5-day forecast table

Sample tickers:

- US: `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `NVDA`
- India (Yahoo format): `RELIANCE.NS`, `TCS.NS`, `INFY.NS`

---

## API Reference

### `POST /predict`

Request:

```json
{
  "ticker": "AAPL"
}
```

Response (example fields):

```json
{
  "ticker": "AAPL",
  "history": [/* last 30 close prices */],
  "predictions": [/* next 5 predicted prices */],
  "metrics": {
    "latest_close": 271.29,
    "predicted_close_5d": 269.36,
    "trend_5d_pct": -0.71,
    "volatility_30d_pct": 1.40,
    "ma10": 270.68,
    "ma50": 260.82,
    "rsi": 61.58
  }
}
```

---

## Model Evaluation (Optional)

Run:

```bash
python train.py
```

Outputs:

- train/test sample counts
- MAE (Mean Absolute Error)
- MAPE (Mean Absolute Percentage Error)

---

## Dataset Requirement

No manual dataset download is required.

- Data is fetched dynamically from Yahoo Finance (`yfinance`)
- Internet connection is required
- You can later add CSV caching for offline reproducibility if needed

---

## Resume Value / Novelty

This project stands out because it is:

- **End-to-end** (data -> model -> API -> dashboard)
- **Practical** (live market data instead of static CSV only)
- **Interpretable** (technical indicators + risk metrics)
- **Product-oriented** (clean UI/UX and usable analytics)

Suggested resume line:

> Built a full-stack stock forecasting dashboard using Flask, scikit-learn, and Chart.js with live Yahoo Finance data, technical indicators, and interactive KPI-based visualization.

---

## Limitations

- Forecasting uses a simple ML approach (Random Forest) and is not a trading system
- No macroeconomic/news sentiment features yet
- Not intended for financial advice

---

## Future Improvements

- Add LSTM/GRU/Transformer comparison
- Add sentiment analysis from financial news
- Add multi-ticker comparison view
- Add export to CSV/PDF report
- Add Docker deployment and CI pipeline

---

## License

This project is for educational and portfolio purposes. Add a formal license (MIT recommended) if publishing publicly.

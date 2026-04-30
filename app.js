let chart;

async function predict() {
    let ticker = document.getElementById("ticker").value.trim().toUpperCase();
    let output = document.getElementById("output");
    let btn = document.getElementById("predictBtn");

    if (!ticker) {
        output.innerText = "Please enter a stock ticker (example: AAPL).";
        return;
    }

    output.innerText = "Loading...";
    btn.disabled = true;

    try {
        let res = await fetch("/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ticker})
        });

        let data = await res.json();

        if (!res.ok || data.error) {
            output.innerText = data.error || "Unable to generate prediction.";
            return;
        }

        output.innerText = `${data.ticker} analyzed successfully.`;
        updateMetrics(data.metrics);
        renderForecastTable(data.predictions);
        drawChart(data.history, data.predictions);
    } catch (err) {
        output.innerText = "Network error. Please try again.";
    } finally {
        btn.disabled = false;
    }
}

function drawChart(history, preds) {
    let ctx = document.getElementById("chart").getContext("2d");
    let labels = Array.from({ length: history.length + preds.length }, (_, i) => i + 1);
    let historySeries = [...history, ...new Array(preds.length).fill(null)];
    let predSeries = [...new Array(history.length - 1).fill(null), history[history.length - 1], ...preds];

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Historical Close",
                    data: historySeries,
                    borderColor: "#6a5ae0",
                    backgroundColor: "rgba(106, 90, 224, 0.15)",
                    borderWidth: 2,
                    tension: 0.35
                },
                {
                    label: "Forecast",
                    data: predSeries,
                    borderColor: "#20b2aa",
                    borderDash: [7, 5],
                    borderWidth: 2,
                    tension: 0.35
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "top"
                }
            }
        }
    });
}

function updateMetrics(metrics) {
    document.getElementById("latestClose").innerText = toMoney(metrics.latest_close);
    document.getElementById("predictedClose").innerText = toMoney(metrics.predicted_close_5d);
    document.getElementById("trend5d").innerText = `${metrics.trend_5d_pct.toFixed(2)}%`;
    document.getElementById("volatility").innerText = `${metrics.volatility_30d_pct.toFixed(2)}%`;
    document.getElementById("movingAverages").innerText = `${toMoney(metrics.ma10)} / ${toMoney(metrics.ma50)}`;
    document.getElementById("rsi").innerText = metrics.rsi.toFixed(2);
    document.getElementById("backtestMae").innerText = metrics.backtest_mae ? toMoney(metrics.backtest_mae) : "-";
    document.getElementById("backtestMape").innerText = metrics.backtest_mape ? `${metrics.backtest_mape.toFixed(2)}%` : "-";
}

function renderForecastTable(predictions) {
    let rows = document.getElementById("forecastRows");
    rows.innerHTML = "";

    predictions.forEach((value, idx) => {
        let tr = document.createElement("tr");
        tr.innerHTML = `<td>Day ${idx + 1}</td><td>${toMoney(value)}</td>`;
        rows.appendChild(tr);
    });
}

function toMoney(value) {
    return `$${Number(value).toFixed(2)}`;
}
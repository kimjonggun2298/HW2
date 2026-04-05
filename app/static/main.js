document.addEventListener("DOMContentLoaded", () => {
    const tickerInput = document.getElementById("ticker-input");
    const analyzeBtn = document.getElementById("analyze-btn");

    const loadingOverlay = document.getElementById("loading-overlay");
    const resultsContainer = document.getElementById("results-container");
    const errorContainer = document.getElementById("error-container");
    const errorMsg = document.getElementById("error-message");

    let predictionChart = null;

    // Enter key support
    tickerInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            analyzeBtn.click();
        }
    });

    analyzeBtn.addEventListener("click", async () => {
        const ticker = tickerInput.value.trim();
        if (!ticker) return;

        // UI Reset
        resultsContainer.classList.add("hidden");
        errorContainer.classList.add("hidden");
        loadingOverlay.classList.remove("hidden");

        try {
            // Fetch Prediction from Backend
            const response = await fetch(`/predict?ticker=${encodeURIComponent(ticker)}&predict_days=30`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Failed to fetch data from the server.");
            }

            renderDashboard(data);
        } catch (error) {
            showError(error.message);
        } finally {
            loadingOverlay.classList.add("hidden");
        }
    });

    function renderDashboard(data) {
        // Update Summary Cards
        document.getElementById("val-ticker").textContent = data.ticker.toUpperCase();

        const lastPrice = data.last_closing_price;
        document.getElementById("val-last-price").textContent = formatCurrency(lastPrice);
        document.getElementById("val-last-date").textContent = `As of ${data.last_closing_date}`;

        const forecastData = data.future_prediction;
        const lastForecastPrice = forecastData[forecastData.length - 1].predicted_price;

        document.getElementById("val-forecast-price").textContent = formatCurrency(lastForecastPrice);

        // Calculate Trend percentage
        const diff = lastForecastPrice - lastPrice;
        const percent = (diff / lastPrice) * 100;
        const trendEl = document.getElementById("val-trend");

        if (diff > 0) {
            trendEl.textContent = `+${formatCurrency(diff)} (+${percent.toFixed(2)}%)`;
            trendEl.className = "card-subtitle trend-up";
        } else {
            trendEl.textContent = `${formatCurrency(diff)} (${percent.toFixed(2)}%)`;
            trendEl.className = "card-subtitle trend-down";
        }

        // Render Chart
        renderChart(data);

        // Render AI Guideline
        if (data.guideline) {
            document.getElementById("val-guideline").textContent = data.guideline;
            document.getElementById("guideline-container").classList.remove("hidden");
        }

        // Show the results container smoothly
        resultsContainer.classList.remove("hidden");
    }

    function renderChart(data) {
        const ctx = document.getElementById("predictionChart").getContext("2d");

        if (predictionChart) {
            predictionChart.destroy();
        }

        const dates = data.future_prediction.map(d => d.date);
        const prices = data.future_prediction.map(d => d.predicted_price);

        // Gradient for line fill
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
        gradient.addColorStop(1, 'rgba(59, 130, 246, 0.01)');

        // Chart.js Configuration
        predictionChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Predicted Price',
                    data: prices,
                    borderColor: '#3b82f6',
                    backgroundColor: gradient,
                    borderWidth: 2,
                    pointBackgroundColor: '#60a5fa',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#f0f2f5', font: { family: 'Inter', size: 13 } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f0f2f5',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: false,
                        cornerRadius: 8,
                        titleFont: { size: 14, weight: 'bold' },
                        bodyFont: { size: 14 },
                        callbacks: {
                            label: function (context) {
                                return `Price: ${formatCurrency(context.parsed.y)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                        ticks: { color: '#94a3b8', maxTicksLimit: 7 }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                        ticks: {
                            color: '#94a3b8',
                            callback: function (value) { return formatCurrency(value); }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
            }
        });
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorContainer.classList.remove("hidden");
    }

    function formatCurrency(val) {
        // Automatically add commas for readability
        return new Intl.NumberFormat('en-US', { style: 'decimal', maximumFractionDigits: 2 }).format(val);
    }
});

# Stock Info Daily Report

## Overview

**Stock Info Daily Report** is a Python project that generates daily stock reports for top NIFTY 50 (India) and S&P 500 (USA) companies. It fetches the latest available stock prices, calculates daily changes, and generates a CSV report. The report is automatically sent to a Discord channel and can also be downloaded on demand via a REST API.

---

## Features

- **Fetches latest stock prices** for top Indian and US companies using Yahoo Finance.
- **Calculates daily change and percentage change** for each stock.
- **Generates a CSV report** with all relevant data.
- **Sends the report to a Discord channel** via webhook.
- **REST API endpoints**:
  - `/health` — Health check endpoint.
  - `/generate-report` — Generate and download the latest report on demand.

---

## Project Structure

```
stock-info/
├── app.py                  # FastAPI app with endpoints
├── daily_stock_report.py   # Main logic for fetching, processing, and reporting
├── tickers.py              # Static ticker lists for India and USA
├── discord_notify.py       # Function to send CSV to Discord
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (Discord webhook, etc.)
└── README.md               # Project documentation
```

---

## Setup Instructions

1. **Clone the repository**

    ```sh
    git clone <your-repo-url>
    cd stock-info
    ```

2. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

3. **Configure environment variables**

    Create a `.env` file in the root directory:

    ```
    DISCORD_WEBHOOK_URL=<your-discord-webhook-url>
    ```

4. **Run the API locally**

    ```sh
    uvicorn app:app --reload
    ```

    - Visit `http://localhost:8000/health` for health check.
    - POST to `http://localhost:8000/generate-report` to generate and download the CSV.

5. **Run the script manually (optional)**

    ```sh
    python daily_stock_report.py
    ```

---

## Deployment (Render.com Example)

1. **Push your code to GitHub.**
2. **Create a new Web Service on [Render](https://render.com/).**
3. **Set the start command:**
    ```
    uvicorn app:app --host 0.0.0.0 --port 10000
    ```
4. **Add your environment variable (`DISCORD_WEBHOOK_URL`).**
5. **(Optional) Add a Render Cron Job** to run `python daily_stock_report.py` daily.

---

## Customization

- **Change the number of stocks:**  
  Edit `TOP_N` in `daily_stock_report.py` to select how many stocks to include (between 12 and 18).
- **Change tickers:**  
  Edit `tickers.py` to update the static lists for India and USA.

---

## License

MIT License

---

## Credits

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [FastAPI](https://fastapi.tiangolo.com/) for the API
- [Render](https://render.com/) for easy deployment

---
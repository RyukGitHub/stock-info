import csv
import logging
from datetime import datetime
import yfinance as yf
from tickers import NIFTY50_TICKERS, SP500_TICKERS
from discord_notify import send_csv_to_discord_webhook
from dotenv import load_dotenv

# ---------------------- Logging Setup ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ---------------------- Ticker Validation ----------------------
def get_valid_tickers(symbols, region, max_count=12):
    valid = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("regularMarketPrice")
            name = info.get("longName") or info.get("shortName") or ""
            if price is not None and name:
                valid.append({"Symbol": symbol, "Name": name})
                logger.info(f"[{region}] Validated: {symbol} ({name})")
                if len(valid) >= max_count:
                    break
            else:
                logger.warning(f"[{region}] Skipping invalid symbol: {symbol}")
        except Exception as e:
            logger.warning(f"[{region}] Validation failed for {symbol}: {e}")
    return valid

# ---------------------- Utilities ----------------------
def get_ist_now():
    return datetime.now().astimezone()

# ---------------------- Fetch Prices ----------------------
def fetch_prices(valid_tickers, region):
    data = []
    for item in valid_tickers:
        symbol = item["Symbol"]
        name = item["Name"]
        try:
            ticker = yf.Ticker(symbol)
            if region == "USA":
                # Use intraday 5-minute interval for USA
                hist = ticker.history(period='1d', interval='5m')
                if len(hist) == 0:
                    raise Exception("No intraday data available")
                price = hist['Close'].iloc[-1]
                price_time = hist.index[-1].strftime("%Y-%m-%d %I:%M %p")
                # For previous close, fallback to daily data
                daily_hist = ticker.history(period='2d')
                prev_close = daily_hist['Close'].iloc[-2] if len(daily_hist) >= 2 else None
            else:
                # Use daily data for India
                hist = ticker.history(period='2d')
                if len(hist) == 0:
                    raise Exception("No daily data available")
                price = hist['Close'].iloc[-1]
                price_time = hist.index[-1].strftime("%Y-%m-%d %I:%M %p")
                prev_close = hist['Close'].iloc[-2] if len(hist) >= 2 else None

            change = price - prev_close if prev_close is not None else None
            change_pct = (change / prev_close) * 100 if prev_close else None

            data.append({
                "Symbol": symbol,
                "Name": name,
                "Price (USD)" if region == "USA" else "Price (INR)": f"{price:.2f}",
                "Previous Close": f"{prev_close:.2f}" if prev_close is not None else "N/A",
                "Change": f"{change:+.2f}" if change is not None else "N/A",
                "Change (%)": f"{change_pct:+.2f}%" if change_pct is not None else "N/A",
                "Latest Price Date": price_time
            })
            logger.info(f"Fetched {symbol}: {price:.2f} (as of {price_time})")
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            data.append({
                "Symbol": symbol,
                "Name": name,
                "Price (USD)" if region == "USA" else "Price (INR)": 'N/A',
                "Previous Close": 'N/A',
                "Change": 'N/A',
                "Change (%)": 'N/A',
                "Latest Price Date": 'N/A'
            })
    return data

# ---------------------- Report Generation ----------------------
def generate_report():
    try:
        # Set to any value between 12 and 18
        TOP_N = 12
        india_symbols = NIFTY50_TICKERS[:TOP_N]
        usa_symbols = SP500_TICKERS[:TOP_N]

        logger.info(f"India symbols: {india_symbols}")
        logger.info(f"USA symbols: {usa_symbols}")

        india_valid = get_valid_tickers(india_symbols, region="India", max_count=TOP_N)
        usa_valid = get_valid_tickers(usa_symbols, region="USA", max_count=TOP_N)

        logger.info(f"Valid India tickers: {india_valid}")
        logger.info(f"Valid USA tickers: {usa_valid}")

        india_data = fetch_prices(india_valid, region="India")
        usa_data = fetch_prices(usa_valid, region="USA")

        now = datetime.now().astimezone()
        date_str = now.strftime("%d-%m-%Y")
        filename = f"stock_report_{date_str}.csv"

        with open(filename, "w", newline="") as file:
            # USA section
            file.write("USA Stock Info\n")
            usa_writer = csv.DictWriter(file, fieldnames=[
                "Symbol", "Name", "Price (USD)", "Previous Close", "Change", "Change (%)", "Latest Price Date"
            ])
            usa_writer.writeheader()
            usa_writer.writerows(usa_data)

            # India section
            file.write("\nINDIA Stock Info\n")
            india_writer = csv.DictWriter(file, fieldnames=[
                "Symbol", "Name", "Price (INR)", "Previous Close", "Change", "Change (%)", "Latest Price Date"
            ])
            india_writer.writeheader()
            india_writer.writerows(india_data)

        logger.info(f"[{now.strftime('%I:%M %p')} IST] CSV report generated: {filename}")

        # Send to Discord
        send_csv_to_discord_webhook(filename)

        # Return the filename for API use
        return filename

    except Exception as e:
        logger.critical(f"Script crashed: {e}")

# ---------------------- Main Execution ----------------------
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    try:
        generate_report()
    except Exception as e:
        logger.critical(f"Script crashed: {e}")

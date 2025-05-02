
import requests
import json
from datetime import datetime
import os
import logging


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(BASE_DIR, "logs", "fetch.log")
CSE_API_URL = "https://www.cse.lk/api/tradeSummary"


os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")


SP20_TICKERS = {
    "CCS.N0000", "LLUB.N0000", "COMB.N0000", "COMB.X0000", "DFCC.N0000", "DIAL.N0000",
    "DIST.N0000", "HNB.N0000", "HNB.X0000", "HAYL.N0000", "HHL.N0000", "JKH.N0000",
    "LIOC.N0000", "LFIN.N0000", "LOFC.N0000", "LOLC.N0000", "MELS.N0000", "NDB.N0000",
    "NTB.N0000", "RCL.N0000", "SAMP.N0000", "VONE.N0000"
}

def is_market_day():
    today = datetime.today()
    return today.weekday() < 5  

def fetch_summary():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.post(CSE_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        json_data = response.json()

        if isinstance(json_data, dict):
            for key in json_data:
                if isinstance(json_data[key], list):
                    return json_data[key]
        elif isinstance(json_data, list):
            return json_data

        logging.error("Unexpected response format from API.")
        return None
    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
        return None

def filter_sp20(data):
    if not isinstance(data, list):
        logging.error("Unexpected data format")
        return []

    filtered = [item for item in data if item.get("symbol") in SP20_TICKERS]
    logging.info(f"Filtered {len(filtered)} S&P SL20 companies.")
    return filtered

def save_data(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    today_str = datetime.today().strftime("%Y-%m-%d")
    file_path = os.path.join(DATA_DIR, f"{today_str}-sp20.json")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved S&P SL20 data to {file_path}")

def main():
    if not is_market_day():
        logging.info("Today is not a market day. Skipping fetch.")
        return

    data = fetch_summary()
    if data:
        sp20_data = filter_sp20(data)
        if sp20_data:
            save_data(sp20_data)
        else:
            logging.warning("No S&P SL20 data found in response.")
    else:
        logging.error("No data fetched.")

if __name__ == "__main__":
    main()

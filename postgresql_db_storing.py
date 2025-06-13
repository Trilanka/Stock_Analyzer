import os
import json
import psycopg2
from datetime import datetime

# Database configuration
DB_NAME = "market"
DB_USER = "postgres"
DB_PASSWORD = "abc"
DB_HOST = "localhost"
DB_PORT = "5432"

# JSON files directory
DATA_FOLDER = "/home/ubuntu/Scrapper/Stock_Analyzer/daily_reports"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Parse "01/JAN/1984" → datetime.date
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%b/%Y").date()
    except Exception:
        return None

# Loop over all JSON files
for filename in os.listdir(DATA_FOLDER):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(DATA_FOLDER, filename)

    with open(file_path, "r") as f:
        data = json.load(f)

    trade_date = data.get("date")
    if not trade_date:
        print(f"⚠️ No 'date' in file: {filename}")
        continue

    # Check if this date already exists in DB
    cur.execute("SELECT 1 FROM daily_market WHERE trade_date = %s LIMIT 1", (trade_date,))
    if cur.fetchone():
        print(f"⏩ Skipping already imported trade_date: {trade_date}")
        continue

    summaries = data.get("market_summary", {}).get("reqTradeSummery", [])
    if not summaries:
        print(f"⚠️ No market summary data in file: {filename}")
        continue

    for entry in summaries:
        company_id = entry["id"]
        name = entry["name"]
        symbol = entry["symbol"]
        issue_date = parse_date(entry["issueDate"])

        # Insert into company table (skip if already exists)
        cur.execute("""
            INSERT INTO company (company_id, name, symbol, issue_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING;
        """, (company_id, name, symbol, issue_date))

        # Insert into daily_market table (skip if already exists)
        cur.execute("""
            INSERT INTO daily_market (
                trade_date, company_id, quantity, percentage_change, change, price,
                previous_close, high, low, last_traded_time, turnover,
                share_volume, trade_volume, market_cap, market_cap_percentage,
                open, closing_price, crossing_volume, crossing_trade_vol, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON CONFLICT (company_id, trade_date) DO NOTHING;
        """, (
            trade_date, company_id, entry["quantity"], entry["percentageChange"], entry["change"], entry["price"],
            entry["previousClose"], entry["high"], entry["low"], entry["lastTradedTime"], entry["turnover"],
            entry["sharevolume"], entry["tradevolume"], entry["marketCap"], entry["marketCapPercentage"],
            entry["open"], entry["closingPrice"], entry["crossingVolume"], entry["crossingTradeVol"], entry["status"]
        ))

    print(f"✅ Data imported for trade_date: {trade_date}")

# Finalize DB work
conn.commit()
cur.close()
conn.close()


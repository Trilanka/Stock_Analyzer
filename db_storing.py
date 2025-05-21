import os
import json
import psycopg2
from datetime import datetime

DB_NAME = "market"
DB_USER = "postgres"
DB_PASSWORD = "abc"  
DB_HOST = "localhost"
DB_PORT = "5432"

DATA_FOLDER = "/home/ubuntu/Scrapper/Stock_Analyzer/daily_reports"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%b/%Y").date()
    except Exception:
        return None


for filename in os.listdir(DATA_FOLDER):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(DATA_FOLDER, filename)
    with open(file_path, "r") as f:
        data = json.load(f)

    trade_date = data["date"]
    summaries = data.get("market_summary", {}).get("reqTradeSummery", [])

    for entry in summaries:
        company_id = entry["id"]
        name = entry["name"]
        symbol = entry["symbol"]
        issue_date = parse_date(entry["issueDate"])

        cur.execute("""
            INSERT INTO company (company_id, name, symbol, issue_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING;
        """, (company_id, name, symbol, issue_date))

        # Insert market data (ignore duplicates)
        cur.execute("""
            INSERT INTO daily_market(
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

conn.commit()
cur.close()
conn.close()
print(f"✅ Data import completed for the trade date - {trade_date}")
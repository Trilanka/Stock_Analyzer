import os
import json
from collections import defaultdict

DATA_DIR = "/home/ubuntu/Scrapper/Stock_Analyzer/daily_reports"

company_data = defaultdict(lambda: {"company_name": "", "history": []})

for filename in sorted(os.listdir(DATA_DIR)):
    if filename.endswith(".json"):
        file_path = os.path.join(DATA_DIR, filename)
        with open(file_path, "r") as f:
            data = json.load(f)
            date = data.get("date", "")

            market_summary = data.get("market_summary", [])
            for entry in market_summary:
                symbol = entry.get("symbol")
                if not symbol:
                    continue
                company_info = company_data[symbol]
                company_info["company_name"] = entry.get("securityName", "")
                company_info["history"].append({
                    "date": date,
                    "close_price": entry.get("closePrice"),
                    "volume": entry.get("volume"),
                    "turnover": entry.get("turnover"),
                    "no_of_trades": entry.get("noOfTrades"),
                    "market_cap": entry.get("marketCap")
                })

# Save final output to one file
with open("structured_company_data.json", "w") as f:
    json.dump(company_data, f, indent=2)

print("[DONE] Data structured and saved to structured_company_data.json")

import os
import json
import re
from collections import defaultdict


DAILY_REPORTS_FOLDER = "daily_reports"
STRUCTURED_FOLDER = "structured_data"

os.makedirs(STRUCTURED_FOLDER, exist_ok=True)

def load_daily_data():
    daily_data = []

    for filename in os.listdir(DAILY_REPORTS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(DAILY_REPORTS_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse {filename}: {e}")
                    continue

                match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
                if match:
                    data["date"] = match.group(0)  
                    daily_data.append(data)
                else:
                    print(f"⚠️ Skipping file with invalid date format: {filename}")

    return daily_data

def structure_company_data(daily_data):
    companies_data = defaultdict(lambda: {
        "name": "",
        "symbol": "",
        "history": [],
        "related_news": set()
    })

    for day in daily_data:
        date = day["date"]
        market_summary = day.get("market_summary", {})
        news = day.get("news", [])

        companies = market_summary.get("reqTradeSummery", [])
        if not isinstance(companies, list):
            print(f"⚠️ Skipping due to invalid market summary format on {date}")
            continue

        for company in companies:
            symbol = company.get("symbol")
            name = company.get("name")
            if not symbol:
                continue

         
            entry = companies_data[symbol]
            entry["name"] = name
            entry["symbol"] = symbol
            entry["history"].append({
                "date": date,
                "price": company.get("price"),
                "change": company.get("change"),
                "percentageChange": company.get("percentageChange"),
                "turnover": company.get("turnover"),
                "volume": company.get("sharevolume"),
                "marketCap": company.get("marketCap")
            })

           
            for article in news:
                title = article.get("title")
                if title:
                    entry["related_news"].add(title)

   
    for company in companies_data.values():
        company["related_news"] = list(company["related_news"])

    return companies_data

def save_structured_data(companies_data):
    output_path = os.path.join(STRUCTURED_FOLDER, "structured_company_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(companies_data, f, indent=2)
    

if __name__ == "__main__":
    daily_data = load_daily_data()
    companies_data = structure_company_data(daily_data)
    save_structured_data(companies_data)

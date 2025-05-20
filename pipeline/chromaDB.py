import os
import json
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


client = chromadb.PersistentClient(path="/Users/trilankasmac/Desktop/Programming/Analyzer/chroma_db")
collection = client.get_or_create_collection("stock_summaries")
client_openai = OpenAI(api_key=OPENAI_API_KEY)
DATA_FOLDER = "/Users/trilankasmac/Desktop/Programming/Analyzer/daily_reports"

### Waste of tokens

# def generate_summary(company_data, date_str):
#     name = company_data["name"]
#     symbol = company_data["symbol"]
#     closing = company_data["closingPrice"]
#     change = company_data["change"]
#     pct_change = company_data["percentageChange"]
#     prev = company_data["previousClose"]
#     high = company_data["high"]
#     low = company_data["low"]
#     volume = company_data["sharevolume"]
#     turnover = company_data["turnover"]
#     market_cap = company_data["marketCap"]

#     return (
#         f"On {date_str}, {name} ({symbol}) closed at Rs. {closing:.2f}, "
#         f"{'up' if change > 0 else 'down'} by Rs. {abs(change):.2f} "
#         f"({pct_change:+.2f}%) from the previous close of Rs. {prev:.2f}. "
#         f"The day's high was Rs. {high:.2f} and the low was Rs. {low:.2f}. "
#         f"A total of {volume:,} shares were traded with a turnover of "
#         f"Rs. {turnover:,.2f}. The market capitalization stood at approximately "
#         f"Rs. {market_cap / 1e9:.2f} billion."
#     )

def embed_text(text):
    response = client_openai.embeddings.create(
        model="text-embedding-3-small", 
        input=[text]
    )
    return response.data[0].embedding

def process_file(filepath):
    filename = os.path.basename(filepath)
    doc_id = filename.replace(".json", "")


    if collection.get(ids=[doc_id], include=[])["ids"]:
        print(f"Skipping {filename} — already embedded.")
        return

    with open(filepath, "r") as f:
        raw = json.load(f)

    sp_sl20_symbols = [
    "COMB.N0000", "JKH.N0000", "DIAL.N0000", "CARG.N0000", "NDB.N0000",
    "SAMP.N0000", "NTB.N0000", "LLUB.N0000", "CINS.N0000", "HNB.N0000",
    "MELS.N0000", "BIL.N0000", "LIOC.N0000", "EXPO.N0000", "PLC.N0000",
    "TJL.N0000", "RICH.N0000", "CTC.N0000", "BFL.N0000", "HAYL.N0000"
    ]

    date_str = doc_id 

    summaries = {}

    for company in raw.get("market_summary", {}).get("reqTradeSummery", []):
        symbol = company.get("symbol")
        if symbol not in sp_sl20_symbols:
            continue

        chroma_id = f"{doc_id}_{symbol}"
        existing = collection.get(ids=[chroma_id])
        if existing and existing["ids"]:
            continue

        summary = generate_summary(company, date_str)
        vector = embed_text(summary)
        collection.add(
            ids=[chroma_id],
            documents=[summary],
            embeddings=[vector],
            metadatas=[{"date": date_str, "symbol": symbol}]
        )
        print(f"Embedded and stored: {chroma_id}")

def main():
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_FOLDER, filename)
            process_file(filepath)




if __name__ == "__main__":
    main()

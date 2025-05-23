import os
import json
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

embedding_model = "text-embedding-ada-002"
JSON_FOLDER = "/home/ubuntu/Scrapper/Stock_Analyzer/news"

chroma_client = chromadb.Client(Settings(
    persist_directory="/home/ubuntu/chromaDB",
    anonymized_telemetry=False
))

collection = chroma_client.get_or_create_collection(name="daily_news")

existing_dates = set()
existing = collection.get(include=["metadatas"])
for meta in existing["metadatas"]:
    if meta and "date" in meta:
        existing_dates.add(meta["date"])

for filename in os.listdir(JSON_FOLDER):
    if not filename.endswith(".json"):
        continue

    file_date = filename.replace(".json", "")
    if file_date in existing_dates:
        print(f"Skipping {filename}, already stored.")
        continue

    file_path = os.path.join(JSON_FOLDER, filename)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        for idx, item in enumerate(data):
            content = item["article_content"]
            response = client.embeddings.create(
                input=[content],
                model=embedding_model
            )
            vector = response.data[0].embedding

            doc_id = f"{file_date}-{idx}"
            collection.add(
                embeddings=[vector],
                documents=[content],
                metadatas=[{
                    "date": item["date"],
                    "title": item["article_title"],
                    "filename": filename
                }],
                ids=[doc_id]
            )
            print(f"Stored article from {filename} with ID {doc_id}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")

try:
    chroma_client.persist()
except AttributeError:
    pass  

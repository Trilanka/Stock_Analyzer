import os
import json
import chromadb
from chromadb.config import Settings

# Path to the folder containing your daily JSON files
JSON_FOLDER = "/home/ubuntu/Scrapper/Stock_Analyzer/news"

# Setup ChromaDB client
chroma_client = chromadb.Client(Settings(
    persist_directory="/home/ubuntu/chromaDB",  # Folder to persist vector DB
    anonymized_telemetry=False
))

# Create or get a collection
collection = chroma_client.get_or_create_collection(name="daily_news")

# Get already inserted document IDs
existing_ids = set(collection.get(include=["metadatas"])["metadatas"])
existing_dates = {meta["date"] for meta in existing_ids if "date" in meta}

# Iterate through JSON files in the folder
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
            doc_id = f"{file_date}-{idx}"
            collection.add(
                documents=[item["article_content"]],
                metadatas=[{"date": item["date"], "title": item["article_title"], "filename": filename}],
                ids=[doc_id]
            )
            print(f"Stored article from {filename} with ID {doc_id}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")

# Persist changes
chroma_client.persist()

import os
import json
from datetime import datetime
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

# OpenAI client
client = OpenAI()
embedding_model = "text-embedding-ada-002"

# Paths
JSON_FOLDER = "/home/ubuntu/Scrapper/Stock_Analyzer/news"
CHROMA_PATH = "/home/ubuntu/Scrapper/Stock_Analyzer/chromaDB"
TODAY = datetime.now().strftime("%Y-%m-%d")
TODAY_FILE = f"{TODAY}.json"
FILE_PATH = os.path.join(JSON_FOLDER, TODAY_FILE)

# Chroma setup
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="daily_news")

# Check if today's file is already processed
existing_ids = set()
existing = collection.get(include=["ids", "metadatas"])
for idx, meta in enumerate(existing["metadatas"]):
    if meta and meta.get("filename") == TODAY_FILE:
        existing_ids.add(existing["ids"][idx])

# Skip if today's JSON is not found
if not os.path.exists(FILE_PATH):
    print(f"⚠️ No file found for today: {TODAY_FILE}. Skipping.")
else:
    print(f"📰 Processing {TODAY_FILE}...")
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            articles = json.load(f)

        added_count = 0
        for i, article in enumerate(articles):
            doc_id = f"{TODAY}-{i}"
            if doc_id in existing_ids:
                continue  # Already added

            content = article.get("article_content", "")
            if not content:
                continue

            response = client.embeddings.create(
                input=[content],
                model=embedding_model
            )
            vector = response.data[0].embedding

            collection.add(
                documents=[content],
                embeddings=[vector],
                metadatas=[{
                    "date": article.get("date"),
                    "title": article.get("article_title"),
                    "filename": TODAY_FILE
                }],
                ids=[doc_id]
            )
            added_count += 1

        print(f"✅ Added {added_count} new articles to Chroma DB.")
    except Exception as e:
        print(f"❌ Failed to process today's file: {e}")

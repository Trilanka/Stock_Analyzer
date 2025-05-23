import chromadb
from chromadb.config import Settings

# Use the same persist directory used when creating/storing the data
chroma_client = chromadb.Client(Settings(
    persist_directory="/home/ubuntu/chromaDB",
    anonymized_telemetry=False
))

# Get the existing collection (do NOT use get_or_create here if you want only existing)
collection = chroma_client.get_collection(name="daily_news")

# Check how many documents are stored
print(f"Total documents stored: {collection.count()}")

# Retrieve some documents to verify
results = collection.get(
    limit=5,
    include=["documents", "metadatas", "ids"]
)

for doc_id, doc, meta in zip(results["ids"], results["documents"], results["metadatas"]):
    print(f"ID: {doc_id}")
    print(f"Title: {meta.get('title')}")
    print(f"Date: {meta.get('date')}")
    print(f"Content snippet: {doc[:100]}")
    print("-" * 20)

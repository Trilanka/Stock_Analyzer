import os
import json
from openai import OpenAI
import chromadb
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = chromadb.PersistentClient(path="/Users/trilankasmac/Desktop/Programming/Analyzer/chroma_db")
collection = client.get_or_create_collection("stock_summaries")
client_openai = OpenAI(api_key=OPENAI_API_KEY)


query = "Give a comment on JKH.N0000 performance"  
response = client_openai.embeddings.create(
    model="text-embedding-3-small",
    input=[query]
)
query_embedding = response.data[0].embedding

    
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)

    
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"Match (distance={dist:.4f}) — {meta['symbol']} on {meta['date']}")
    print(doc)
        
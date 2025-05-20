import os
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_openai = OpenAI(api_key=OPENAI_API_KEY)

client = chromadb.PersistentClient(path="/Users/trilankasmac/Desktop/Programming/Analyzer/chroma_db")
collection = client.get_or_create_collection("stock_summaries")


question = "Do you know dividend for lanka ioc company"  


response = client_openai.embeddings.create(
    model="text-embedding-3-small",
    input=[question]
)
query_embedding = response.data[0].embedding


results = collection.query(
    query_embeddings=[query_embedding],
    n_results=20,
    include=["documents", "metadatas"]
)


retrieved_info = []
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    retrieved_info.append(f"{meta['date']}: {doc}")
context = "\n".join(retrieved_info)


# prompt = f"""
# The user asked: "{question}"

# You are given stock summaries for different days for the company ioc sri lanka.

# Extract a clean list of (date, closing_price) tuples ONLY from the summaries. 
# Format: [("YYYY-MM-DD", 123.45), ...] and return only this list with the dates order must be past to present — no explanation.

# Summaries:
# {context}
# """


prompt = f"""
The user asked: "{question}"

You are given stock summaries for different days for the company ioc sri lanka.

give a proper answer to the user question by thinking and using data feed to you if needed also

Summaries:
{context}
"""



response = client_openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0
)


print("Extracted values:")
print(response.choices[0].message.content)

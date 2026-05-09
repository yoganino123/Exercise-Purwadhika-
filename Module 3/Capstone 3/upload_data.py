# upload_data.py (versi Resume)
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# 1. Load CSV
df = pd.read_csv("Dataset/RESUME/Resume.csv")
df = df.fillna("")

# Ambil sample supaya tidak terlalu banyak (opsional, hemat token)
# df = df.sample(200, random_state=42)

# 2. Ubah tiap baris menjadi Document
documents = []
for _, row in df.iterrows():
    content = (
        f"Category: {row['Category']}\n"
        f"Resume:\n{row['Resume_str'][:2000]}"  # batasi panjang teks
    )
    metadata = {
        "id": str(row["ID"]),
        "category": row["Category"],
    }
    documents.append(Document(page_content=content, metadata=metadata))

print(f"Total dokumen: {len(documents)}")

# 3. Upload ke Qdrant
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY
)

collection_name = "resumes"

qdrant = QdrantVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name=collection_name,
)

print("Upload selesai!")
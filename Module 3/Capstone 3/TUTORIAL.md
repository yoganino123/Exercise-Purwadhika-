# Tutorial Lengkap Capstone Project Module 3

## RAG Chatbot Agent dengan LangChain, Qdrant & Streamlit

---

## Daftar Isi

1. [Overview &amp; Poin Penilaian](#1-overview--poin-penilaian)
2. [Pembagian Dataset](#2-pembagian-dataset)
3. [Setup Environment](#3-setup-environment)
4. [Struktur Project](#4-struktur-project)
5. [Membuat Vector Database (Qdrant Cloud)](#5-membuat-vector-database-qdrant-cloud)
6. [Script Upload Data ke Qdrant](#6-script-upload-data-ke-qdrant)
7. [Membuat RAG Tool](#7-membuat-rag-tool)
8. [Membuat Agent dengan LangChain/LangGraph](#8-membuat-agent-dengan-langchainlanggraph)
9. [Menyusun Prompt yang Optimal](#9-menyusun-prompt-yang-optimal)
10. [Integrasi dengan Streamlit](#10-integrasi-dengan-streamlit)
11. [Deploy ke Streamlit Cloud](#11-deploy-ke-streamlit-cloud)
12. [Checklist Submission](#12-checklist-submission)
13. [Tips Mendapatkan Nilai Lebih dari 75](#13-tips-mendapatkan-nilai-lebih-dari-75)

---

## 1. Overview & Poin Penilaian

Capstone Project Module 3 meminta kamu membangun sebuah **mini aplikasi chatbot** berbasis RAG (Retrieval-Augmented Generation) yang:

- Menggunakan **Qdrant Cloud** sebagai vector database
- Menggunakan **OpenAI** untuk embedding dan LLM
- Dibangun dengan **LangChain + LangGraph** sebagai framework agent
- Memiliki **chat history** minimal 3 percakapan ke belakang
- Di-deploy ke **Streamlit Community Cloud**

| Komponen                   | Bobot |
| -------------------------- | ----- |
| Video Penjelasan           | 25%   |
| Pembuatan Vector Database  | 10%   |
| Pembuatan RAG Tool         | 10%   |
| Pembuatan Agent            | 20%   |
| Penyusunan Prompt          | 10%   |
| Integrasi Dengan Streamlit | 25%   |

> **Catatan:** Jika kamu hanya mengikuti contoh (basis minimum), nilai maksimum tiap komponen adalah **75**. Tambahkan kompleksitas kreatif untuk nilai lebih tinggi.

---

## 2. Pembagian Dataset

| Nama                          | Dataset    |
| ----------------------------- | ---------- |
| Andy Kurniawan                | IMDB Movie |
| Yusuf Averroes Sungkar        | Resume     |
| Salomo Agus Ardianto Purba    | IMDB Movie |
| Vannesa Lam                   | IMDB Movie |
| Indri Anjar Kartika Sari      | IMDB Movie |
| Ahmad Zidan Alfa Robby        | IMDB Movie |
| Ade Reni Hutabarat            | Resume     |
| Rahardian Yoganino Pradipta   | IMDB Movie |
| Nabeel Farvez Fayzulhaq       | Resume     |
| Ivan Dwi Hascaryo Ardynugraha | Resume     |
| Ikhsani Taufiqullah Hasan     | Resume     |

### Dataset yang Tersedia:

- **IMDB Movie** → `Dataset/IMDB Movie/imdb_top_1000.csv`
  - Kolom: `Series_Title`, `Released_Year`, `Certificate`, `Runtime`, `Genre`, `IMDB_Rating`, `Overview`, `Meta_score`, `Director`, `Star1-4`, `No_of_votes`, `Gross`
- **Resume** → `Dataset/RESUME/Resume.csv`
  - Kolom: `ID`, `Resume_str`, `Resume_html`, `Category`
  - Kategori: HR, Designer, IT, Teacher, Advocate, Business-Development, Healthcare, dll.

---

## 3. Setup Environment

### 3.1 Install Dependencies

```bash
pip install streamlit langchain langchain-openai langchain-qdrant langchain-core python-dotenv openai qdrant-client langgraph
```

Atau jika ada `requirements.txt`:

```bash
pip install -r "Example Code/requirements.txt"
pip install langgraph  # tambahan yang wajib untuk agent
```

### 3.2 Buat File `.env` (untuk development lokal)

Buat file `.env` di folder `Capstone 3/`:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
QDRANT_URL=https://xxxx.qdrant.tech
QDRANT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

> **PENTING:** Jangan pernah commit file `.env` ke GitHub! Tambahkan ke `.gitignore`.

### 3.3 Buat `.gitignore`

```
.env
__pycache__/
*.pyc
.venv/
```

### 3.4 Dapatkan API Keys

> Untuk panduan lengkap mendapatkan OpenAI API Key (buat akun, top-up kredit, buat key, estimasi biaya, dan keamanan), lihat: **[SETUP_OPENAI.md](SETUP_OPENAI.md)**

**OpenAI API Key — ringkasan:**

1. Buka https://platform.openai.com/api-keys
2. Daftar / login → tambahkan kredit minimal $5 USD di menu **Billing**
3. Klik **"+ Create new secret key"** → beri nama `capstone-3-project`
4. Salin key (`sk-proj-xxx...`) — **hanya tampil sekali!**

**Qdrant Cloud:**

1. Buka https://cloud.qdrant.io/
2. Buat akun / login
3. Klik **"Create Cluster"** → pilih Free Tier
4. Setelah cluster siap, klik cluster kamu → **API Keys** → buat key baru
5. Salin **Cluster URL** dan **API Key**

---

## 4. Struktur Project

```
Capstone 3/
├── main.py              ← file utama Streamlit (kerjakan di sini)
├── upload_data.py       ← script untuk upload data ke Qdrant (buat sekali)
├── .env                 ← API keys (JANGAN di-commit)
├── .gitignore
├── requirements.txt
├── TUTORIAL.md          ← file ini
├── Dataset/
│   ├── IMDB Movie/
│   │   └── imdb_top_1000.csv
│   └── RESUME/
│       └── Resume.csv
└── Example Code/
    └── main.py          ← contoh referensi
```

---

## 5. Membuat Vector Database (Qdrant Cloud)

Vector Database adalah tempat menyimpan data dalam bentuk **embedding** (vektor numerik). Ketika user bertanya, query-nya diubah jadi vektor lalu dicari dokumen yang paling mirip.

### Alur:

```
CSV Data → Teks per baris → OpenAI Embedding → Qdrant Cloud
```

### Langkah di Qdrant Cloud:

1. Login ke https://cloud.qdrant.io/
2. Buat cluster baru (Free tier: 1 cluster, 1GB)
3. Buat **Collection** baru:
   - Nama collection: bebas, misal `imdb_movies` atau `resumes`
   - Vector size: `1536` (untuk model `text-embedding-3-small`)
   - Distance: `Cosine`

> Collection akan otomatis terbuat jika menggunakan `QdrantVectorStore.from_documents()`.

---

## 6. Script Upload Data ke Qdrant

Buat file `upload_data.py` — **jalankan hanya sekali** untuk mengisi vector database.

### Untuk Dataset IMDB Movie:

```python
# upload_data.py
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.schema import Document

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# 1. Load CSV
df = pd.read_csv("Dataset/IMDB Movie/imdb_top_1000.csv")
df = df.fillna("")

# 2. Ubah tiap baris menjadi Document (teks + metadata)
documents = []
for _, row in df.iterrows():
    content = (
        f"Title: {row['Series_Title']}\n"
        f"Year: {row['Released_Year']}\n"
        f"Genre: {row['Genre']}\n"
        f"Rating: {row['IMDB_Rating']}\n"
        f"Director: {row['Director']}\n"
        f"Stars: {row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}\n"
        f"Overview: {row['Overview']}\n"
        f"Runtime: {row['Runtime']}\n"
        f"Certificate: {row['Certificate']}\n"
        f"Meta Score: {row['Meta_score']}\n"
        f"Votes: {row['No_of_votes']}\n"
        f"Gross: {row['Gross']}"
    )
    metadata = {
        "title": row["Series_Title"],
        "year": str(row["Released_Year"]),
        "genre": row["Genre"],
        "rating": str(row["IMDB_Rating"]),
        "director": row["Director"],
    }
    documents.append(Document(page_content=content, metadata=metadata))

print(f"Total dokumen: {len(documents)}")

# 3. Buat embedding dan upload ke Qdrant
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY
)

collection_name = "imdb_movies"  # ganti sesuai kebutuhan

qdrant = QdrantVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name=collection_name,
)

print("Upload selesai! Data berhasil masuk ke Qdrant.")
```

### Untuk Dataset Resume:

```python
# upload_data.py (versi Resume)
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.schema import Document

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
```

### Cara Menjalankan Upload:

```bash
# Pastikan virtual environment aktif
cd "Module 3/Capstone 3"
python upload_data.py
```

> Upload hanya perlu dilakukan **satu kali**. Setelah data ada di Qdrant, kamu cukup query tanpa upload ulang.

---

## 7. Membuat RAG Tool

RAG Tool adalah fungsi yang dieksekusi oleh agent ketika perlu mencari informasi dari vector database.

```python
# Di main.py

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.tools import tool

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY
)

collection_name = "imdb_movies"  # sesuaikan dengan collection kamu

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name=collection_name,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

@tool
def search_movie_info(query: str) -> str:
    """
    Gunakan tool ini untuk mencari informasi film dari database IMDB.
    Input adalah pertanyaan atau kata kunci tentang film.
    Tool ini akan mengembalikan detail film yang relevan.
    """
    results = qdrant.similarity_search(query, k=5)
    if not results:
        return "Tidak ditemukan informasi yang relevan."

    output = []
    for doc in results:
        output.append(doc.page_content)

    return "\n\n---\n\n".join(output)
```

### Tips RAG Tool:

- Deskripsi tool (`docstring`) sangat penting — agent membaca deskripsi ini untuk memutuskan kapan tool dipakai
- `k=5` artinya ambil 5 dokumen paling mirip. Bisa dinaikkan untuk hasil lebih lengkap
- Bisa tambahkan filter metadata: `qdrant.similarity_search(query, k=5, filter={"genre": "Action"})`

---

## 8. Membuat Agent dengan LangChain/LangGraph

### Arsitektur: Single Agent dengan RAG Tool

```python
# main.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Inisialisasi LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0.3
)

# Daftar tools yang diberikan ke agent
tools = [search_movie_info]  # RAG tool dari langkah 7

# System prompt (lihat bagian 9)
SYSTEM_PROMPT = """..."""  # isi di langkah 9

# Buat agent menggunakan LangGraph
agent = create_react_agent(
    model=llm,
    tools=tools,
)

def chat_agent(user_question: str, chat_history: list) -> dict:
    """
    Fungsi utama untuk memanggil agent.

    Args:
        user_question: Pertanyaan dari user
        chat_history: List pesan sebelumnya [{"role": "human/ai", "content": "..."}]

    Returns:
        dict berisi answer, token usage, tool messages
    """
    # Susun messages: system + history + pertanyaan baru
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    # Tambahkan history (maks 6 pesan terakhir = 3 percakapan)
    for msg in chat_history[-6:]:
        if msg["role"] == "Human":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    # Tambahkan pertanyaan terbaru
    messages.append(HumanMessage(content=user_question))

    # Jalankan agent
    result = agent.invoke({"messages": messages})

    # Ambil jawaban
    answer = result["messages"][-1].content

    # Hitung token usage
    total_input_tokens = 0
    total_output_tokens = 0
    tool_messages = []

    for message in result["messages"]:
        # Hitung token
        if hasattr(message, "response_metadata"):
            meta = message.response_metadata
            if "usage_metadata" in meta:
                total_input_tokens += meta["usage_metadata"].get("input_tokens", 0)
                total_output_tokens += meta["usage_metadata"].get("output_tokens", 0)
            elif "token_usage" in meta:
                total_input_tokens += meta["token_usage"].get("prompt_tokens", 0)
                total_output_tokens += meta["token_usage"].get("completion_tokens", 0)

        # Kumpulkan tool messages
        from langchain_core.messages import ToolMessage
        if isinstance(message, ToolMessage):
            tool_messages.append(message.content)

    # Estimasi biaya (dalam Rupiah)
    # gpt-4o-mini: $0.15/1M input tokens, $0.60/1M output tokens
    # Asumsi kurs Rp 17.000/USD
    price_idr = 17_000 * (total_input_tokens * 0.15 + total_output_tokens * 0.6) / 1_000_000

    return {
        "answer": answer,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "price_idr": price_idr,
        "tool_messages": tool_messages,
    }
```

### Arsitektur: Multi-Agent (Supervisor Pattern) — Nilai Lebih Tinggi

```python
# Contoh arsitektur supervisor multi-agent
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
import operator

# Agent spesialis
movie_search_agent = create_react_agent(llm, tools=[search_movie_info])
# recommendation_agent = create_react_agent(llm, tools=[recommend_movies])  # contoh agent lain

class SupervisorState(TypedDict):
    messages: Annotated[list, operator.add]
    next_agent: str

def supervisor_node(state: SupervisorState):
    """Supervisor memutuskan agent mana yang dipanggil."""
    # Logic routing berdasarkan intent user
    last_message = state["messages"][-1].content.lower()

    if any(word in last_message for word in ["cari", "film", "movie", "siapa", "apa"]):
        return {"next_agent": "movie_search"}
    else:
        return {"next_agent": "end"}

# ... (bangun graph dengan StateGraph)
```

---

## 9. Menyusun Prompt yang Optimal

Prompt yang baik adalah kunci agar agent:

1. Tahu **kapan** menggunakan RAG tool
2. Menjawab dengan format yang **konsisten**
3. Menolak pertanyaan **di luar konteks** dengan sopan

### Template System Prompt (IMDB):

```python
SYSTEM_PROMPT = """Kamu adalah asisten ahli film yang bernama CineBot.
Tugasmu adalah menjawab pertanyaan tentang film berdasarkan database IMDB Top 1000.

ATURAN:
1. Selalu gunakan tool `search_movie_info` untuk mencari informasi film sebelum menjawab.
2. Jawab HANYA berdasarkan informasi yang ditemukan dari tool. Jangan mengarang fakta.
3. Jika informasi tidak ditemukan di database, sampaikan dengan jujur:
   "Maaf, saya tidak menemukan informasi tersebut di database."
4. Untuk pertanyaan yang tidak berkaitan dengan film, tolak dengan sopan.
5. Sertakan detail seperti: judul, tahun, genre, rating, sutradara, dan bintang bila relevan.
6. Gunakan bahasa Indonesia yang ramah dan mudah dipahami.
7. Jika user menanyakan konteks dari percakapan sebelumnya, gunakan chat history yang tersedia.

Format jawaban yang baik:
- Mulai dengan ringkasan singkat
- Sertakan detail penting
- Akhiri dengan saran atau pertanyaan lanjutan jika perlu
"""
```

### Template System Prompt (Resume):

```python
SYSTEM_PROMPT = """Kamu adalah asisten HR yang bernama ResumeBot.
Tugasmu adalah membantu pengguna mencari dan menganalisis resume dari berbagai kategori pekerjaan.

ATURAN:
1. Selalu gunakan tool `search_resume` untuk mencari resume yang relevan sebelum menjawab.
2. Jawab berdasarkan data yang ditemukan dari tool, jangan mengarang informasi.
3. Jika tidak ada resume yang cocok, sampaikan dengan jelas.
4. Untuk pertanyaan di luar topik resume/karir, tolak dengan sopan.
5. Tampilkan kategori, skill utama, dan pengalaman relevan dari resume yang ditemukan.
6. Jaga konteks percakapan — jika user melanjutkan diskusi tentang kandidat sebelumnya, ingat konteksnya.

Kamu memiliki akses ke resume dari kategori:
HR, Designer, IT, Teacher, Advocate, Business-Development, Healthcare, Fitness,
Agriculture, BPO, Sales, Consultant, Digital-Media, Automobile, Chef, Finance,
Apparel, Engineering, Accountant, Construction, Public-Relations, Banking, Arts, Aviation
"""
```

---

## 10. Integrasi dengan Streamlit

### Struktur `main.py` Lengkap

```python
# main.py - Versi Lengkap

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Untuk production (Streamlit Cloud), gunakan st.secrets
# Untuk local dev, gunakan os.getenv dari .env
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
QDRANT_URL = st.secrets.get("QDRANT_URL", os.getenv("QDRANT_URL"))
QDRANT_API_KEY = st.secrets.get("QDRANT_API_KEY", os.getenv("QDRANT_API_KEY"))

# --- IMPORT DAN SETUP (langkah 7 & 8 di atas) ---
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

# ... (paste kode dari langkah 7 dan 8)

# ============================================================
# STREAMLIT APP
# ============================================================

st.set_page_config(
    page_title="🎬 CineBot - IMDB Movie Assistant",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CineBot - IMDB Movie Assistant")
st.caption("Tanya apa saja tentang 1000 film terbaik versi IMDB!")

# Sidebar: informasi & tombol reset
with st.sidebar:
    st.header("ℹ️ Tentang CineBot")
    st.markdown("""
    CineBot menggunakan teknologi RAG (Retrieval-Augmented Generation)
    untuk menjawab pertanyaan berdasarkan database IMDB Top 1000.

    **Contoh pertanyaan:**
    - Film action terbaik dari tahun 2000-an?
    - Siapa sutradara film The Dark Knight?
    - Rekomendasikan film dengan rating di atas 9.0
    """)

    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**Dibuat dengan:**")
    st.markdown("- LangChain + LangGraph")
    st.markdown("- OpenAI GPT-4o-mini")
    st.markdown("- Qdrant Vector DB")
    st.markdown("- Streamlit")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari user
if prompt := st.chat_input("Tanya tentang film..."):
    # Ambil history untuk dikirim ke agent (max 6 pesan = 3 percakapan)
    chat_history = st.session_state.messages[-6:]

    # Tampilkan pesan user
    with st.chat_message("Human"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "Human", "content": prompt})

    # Panggil agent dan tampilkan jawaban
    with st.chat_message("AI"):
        with st.spinner("Sedang mencari informasi..."):
            response = chat_agent(prompt, chat_history)

        answer = response["answer"]
        st.markdown(answer)
        st.session_state.messages.append({"role": "AI", "content": answer})

    # Expander: bukti RAG (dokumen yang diambil)
    if response["tool_messages"]:
        with st.expander("📚 Dokumen yang Diambil dari Vector DB (RAG)", expanded=False):
            for i, doc in enumerate(response["tool_messages"], 1):
                st.text(f"[Dokumen {i}]\n{doc[:500]}...")

    # Expander: chat history
    with st.expander("💬 Chat History", expanded=False):
        for msg in chat_history:
            st.text(f"{msg['role']}: {msg['content'][:200]}")

    # Expander: usage details
    with st.expander("📊 Usage Details", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Input Tokens", response["total_input_tokens"])
        with col2:
            st.metric("Output Tokens", response["total_output_tokens"])
        with col3:
            st.metric("Estimasi Biaya", f"Rp {response['price_idr']:.4f}")
```

### Menjalankan Streamlit Secara Lokal

```bash
cd "Module 3/Capstone 3"
streamlit run main.py
```

Buka browser di `http://localhost:8501`

---

## 11. Deploy ke Streamlit Cloud

### Langkah-langkah:

**1. Buat `requirements.txt` di root folder Capstone 3:**

```
streamlit
langchain
langchain-openai
langchain-qdrant
langchain-core
langgraph
python-dotenv
openai
qdrant-client
pandas
```

**2. Upload ke GitHub:**

```bash
# Di folder Capstone 3
git init
git add main.py requirements.txt
# JANGAN add .env !!!
git commit -m "Capstone 3: RAG Chatbot"
git remote add origin https://github.com/username/capstone3.git
git push -u origin main
```

**3. Deploy di Streamlit Cloud:**

1. Buka https://share.streamlit.io/
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository, branch, dan file: `main.py`
5. Klik **"Advanced settings"** → **"Secrets"**
6. Tambahkan secrets:
   ```toml
   OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
   QDRANT_URL = "https://xxxx.qdrant.tech"
   QDRANT_API_KEY = "xxxxxxxxxxxx"
   ```
7. Klik **"Deploy!"**

Setelah deploy, kamu mendapatkan URL publik seperti:
`https://namaapp.streamlit.app`

---

## 12. Checklist Submission

Sebelum submit, pastikan semua item ini terpenuhi:

### Teknis

- [ ] Vector database sudah terisi data (upload berhasil)
- [ ] RAG tool berfungsi (agent berhasil memanggil tool)
- [ ] Agent bisa menjawab pertanyaan berdasarkan data di Qdrant (bukan hallusinasi)
- [ ] Chat history minimal 3 percakapan ke belakang berfungsi
- [ ] Token usage ditampilkan di Streamlit
- [ ] Ada expander/section yang menunjukkan dokumen yang diambil dari RAG
- [ ] API keys TIDAK ada di source code yang di-upload ke GitHub
- [ ] Aplikasi berhasil di-deploy di Streamlit Cloud dengan link publik

### Submission

- [ ] Video penjelasan sudah direkam (maks 15 menit, kamera aktif)
- [ ] Video di-upload ke YouTube/Google Drive/Dropbox dengan akses publik
- [ ] Kode di-upload ke GitHub
- [ ] Google Forms sudah diisi dengan:
  - [ ] Link GitHub
  - [ ] Link Streamlit Cloud
  - [ ] Link video
- [ ] Email konfirmasi dari sistem sudah diterima (cek folder spam)

---

## 13. Tips Mendapatkan Nilai Lebih dari 75

Nilai 75 adalah basis minimum (mengikuti contoh). Untuk nilai lebih tinggi:

### Vector Database (melebihi minimum)

- Tambahkan **filtering metadata** saat retrieve (misal: filter by genre, year, category)
- Gunakan **hybrid search** (kombinasi keyword + semantic)
- Upload lebih banyak data atau data yang lebih kaya

### RAG Tool (melebihi minimum)

- Buat **lebih dari 1 tool** dengan fungsi berbeda:
  - `search_by_genre()` — mencari film berdasarkan genre
  - `get_top_rated()` — mengambil film dengan rating tertinggi
  - `search_by_director()` — mencari berdasarkan sutradara
- Tambahkan **reranking** untuk meningkatkan akurasi

### Agent (melebihi minimum)

- Implementasi **multi-agent** (supervisor + sub-agents)
- Tambahkan **state management** yang lebih kompleks dengan LangGraph
- Gunakan **memory** jangka panjang (bukan hanya session)

### Prompt (melebihi minimum)

- Prompt dengan **few-shot examples** (contoh Q&A di dalam prompt)
- Prompt dengan **chain-of-thought** (minta agent berpikir step-by-step)
- Tambahkan **guardrails** untuk menolak pertanyaan berbahaya

### Streamlit (melebihi minimum)

Tampilan UI yang menarik dengan custom CSS

Tambahkan **fitur filter/pencarian** langsung di UI

Visualisasi data (chart rating, distribusi genre, dll)

Mode **streaming** untuk jawaban agent (terlihat live)

**Authentication** sederhana (password page)

---

## Referensi

- [LangChain Docs](https://python.langchain.com/docs/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Contoh Aplikasi Capstone 3](https://capstone-3.streamlit.app/)
- [OpenAI API Docs](https://platform.openai.com/docs/)

---

> **Ingat:** Jangan sertakan `api_key`, `password`, atau informasi sensitif apapun dalam kode yang di-upload ke GitHub atau ditampilkan di video!

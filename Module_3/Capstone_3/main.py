import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langgraph.prebuilt import create_react_agent

# Muat variabel environment lokal (.env) untuk mode development.
load_dotenv()


def apply_custom_ui() -> None:
	# Styling UI untuk memperkuat tampilan profesional saat demo video.
	st.markdown(
		"""
		<style>
		@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=IBM+Plex+Mono:wght@500&display=swap');

		:root {
			--bg-1: #f2f7f7;
			--bg-2: #e7f0ee;
			--card: #ffffff;
			--text: #142026;
			--muted: #49616d;
			--brand: #0d7c66;
			--brand-soft: #d8efe9;
			--line: #d7e6e3;
		}

		html, body, [class*="css"], [data-testid="stAppViewContainer"] {
			font-family: 'Plus Jakarta Sans', sans-serif;
		}

		[data-testid="stAppViewContainer"] {
			background:
				radial-gradient(circle at 15% 12%, #d8efe9 0, transparent 32%),
				radial-gradient(circle at 92% 6%, #d7ecf6 0, transparent 26%),
				linear-gradient(160deg, var(--bg-1), var(--bg-2));
		}

		.block-container {
			padding-top: 1.4rem;
			padding-bottom: 1.25rem;
			max-width: 1160px;
		}

		.block-container > div {
			gap: 0.95rem;
		}

		.hero {
			background: linear-gradient(135deg, #ffffff 0%, #f4fbf9 100%);
			border: 1px solid var(--line);
			border-radius: 18px;
			padding: 1.2rem 1.3rem;
			box-shadow: 0 10px 28px rgba(17, 42, 53, 0.08);
			animation: fade-slide 460ms ease-out;
		}

		.hero h1 {
			margin: 0;
			font-size: clamp(1.45rem, 2.3vw, 2rem);
			letter-spacing: -0.02em;
			color: var(--text);
		}

		.hero p {
			margin: 0.35rem 0 0;
			color: var(--muted);
			font-size: 0.95rem;
		}

		.badge-row {
			display: flex;
			gap: 0.55rem;
			flex-wrap: wrap;
			margin-top: 0.85rem;
		}

		.badge {
			background: var(--brand-soft);
			color: #0a5d4d;
			border: 1px solid #c4e3db;
			padding: 0.26rem 0.6rem;
			border-radius: 999px;
			font-size: 0.76rem;
			font-weight: 700;
		}

		.metric-card {
			background: var(--card);
			border: 1px solid var(--line);
			border-radius: 12px;
			padding: 0.7rem 0.85rem;
			box-shadow: 0 6px 16px rgba(26, 54, 65, 0.06);
			margin-top: 0.15rem;
		}

		.metric-label {
			font-size: 0.77rem;
			color: var(--muted);
			margin-bottom: 0.18rem;
		}

		.metric-value {
			font-family: 'IBM Plex Mono', monospace;
			font-size: 0.93rem;
			color: var(--text);
			font-weight: 600;
		}

		section[data-testid="stSidebar"] {
			background: linear-gradient(180deg, #0f2a35 0%, #0d2029 100%);
			border-right: 1px solid #143645;
		}

		section[data-testid="stSidebar"] .stButton > button {
			width: 100%;
			background: #0d7c66;
			color: #ffffff;
			border: 1px solid #14a082;
			font-weight: 700;
			border-radius: 10px;
			padding: 0.45rem 0.7rem;
		}

		section[data-testid="stSidebar"] .stButton > button:hover {
			background: #0b6a58;
			color: #ffffff;
			border-color: #0ea585;
		}

		section[data-testid="stSidebar"] .stButton > button:focus {
			box-shadow: 0 0 0 0.2rem rgba(20, 160, 130, 0.32);
		}

		div[data-testid="column"] .stButton > button {
			border-radius: 10px;
			padding: 0.48rem 0.55rem;
		}

		section[data-testid="stSidebar"] * {
			color: #e8f2f7;
		}

		.sidebar-card {
			background: rgba(255, 255, 255, 0.08);
			border: 1px solid rgba(255, 255, 255, 0.16);
			border-radius: 12px;
			padding: 0.75rem;
			font-size: 0.88rem;
		}

		[data-testid="stChatMessage"] {
			border-radius: 14px;
			border: 1px solid var(--line);
			background: #ffffff;
			box-shadow: 0 5px 18px rgba(16, 43, 52, 0.06);
			padding-top: 0.2rem;
			padding-bottom: 0.2rem;
		}

		[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
		[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"] {
			margin-top: 0.15rem;
		}

		[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
			flex-direction: row-reverse;
			justify-content: flex-start;
		}

		[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
			flex-direction: row;
			justify-content: flex-start;
		}

		[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:last-child {
			max-width: 78%;
			margin-left: auto;
		}

		[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:last-child {
			max-width: 78%;
			margin-right: auto;
		}

		[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
			text-align: right;
		}

		[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
			text-align: left;
		}

		[data-testid="stExpander"] {
			border: 1px solid var(--line);
			border-radius: 12px;
			background: #ffffff;
			margin-top: 0.45rem;
		}

		[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
			margin-bottom: 0.12rem;
		}

		@keyframes fade-slide {
			from {
				opacity: 0;
				transform: translateY(9px);
			}
			to {
				opacity: 1;
				transform: translateY(0);
			}
		}

		@media (max-width: 768px) {
			.block-container {
				padding-top: 1rem;
				padding-left: 0.8rem;
				padding-right: 0.8rem;
				padding-bottom: 0.9rem;
			}
			.hero {
				padding: 1rem;
			}
			.block-container > div {
				gap: 0.72rem;
			}

			[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:last-child,
			[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:last-child {
				max-width: 100%;
			}
		}
		</style>
		""",
		unsafe_allow_html=True,
	)

def get_config_value(name: str) -> str | None:
	"""Try Streamlit secrets first, then fallback to local .env."""
	# Prioritaskan Streamlit secrets (deploy), lalu fallback ke .env (lokal).
	try:
		return st.secrets[name]
	except Exception:
		return os.getenv(name)


# For Streamlit Cloud use st.secrets; for local development fallback to .env
OPENAI_API_KEY = get_config_value("OPENAI_API_KEY")
QDRANT_URL = get_config_value("QDRANT_URL")
QDRANT_API_KEY = get_config_value("QDRANT_API_KEY")

# Validasi environment agar aplikasi gagal lebih awal dengan pesan yang jelas.
REQUIRED_VARS = {
	"OPENAI_API_KEY": OPENAI_API_KEY,
	"QDRANT_URL": QDRANT_URL,
	"QDRANT_API_KEY": QDRANT_API_KEY,
}

missing_vars = [name for name, value in REQUIRED_VARS.items() if not value]
if missing_vars:
	st.set_page_config(page_title="ResumeBot", page_icon="📄")
	st.error(
		"Environment variable belum lengkap: " + ", ".join(missing_vars) + ". "
		"Isi di .env (lokal) atau Streamlit secrets (production)."
	)
	st.stop()

# Komponen embedding untuk mengubah query/resume menjadi vektor semantik.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)

# Collection Qdrant yang digunakan untuk retrieval resume.
collection_name = "resumes"
# Koneksi ke koleksi yang sudah ada (hasil ingestion dari upload_data.py).
qdrant = QdrantVectorStore.from_existing_collection(
	embedding=embeddings,
	collection_name=collection_name,
	url=QDRANT_URL,
	api_key=QDRANT_API_KEY,
)

# Kamus normalisasi kategori agar query user (mis. "business development")
# tetap cocok dengan label metadata category pada dataset.
KNOWN_CATEGORIES = {
	"hr": "HR",
	"designer": "Designer",
	"it": "IT",
	"teacher": "Teacher",
	"advocate": "Advocate",
	"business-development": "Business-Development",
	"business development": "Business-Development",
	"healthcare": "Healthcare",
	"fitness": "Fitness",
	"agriculture": "Agriculture",
	"bpo": "BPO",
	"sales": "Sales",
	"consultant": "Consultant",
	"digital-media": "Digital-Media",
	"digital media": "Digital-Media",
	"automobile": "Automobile",
	"chef": "Chef",
	"finance": "Finance",
	"apparel": "Apparel",
	"engineering": "Engineering",
	"accountant": "Accountant",
	"construction": "Construction",
	"public-relations": "Public-Relations",
	"public relations": "Public-Relations",
	"banking": "Banking",
	"arts": "Arts",
	"aviation": "Aviation",
}


def extract_category_from_text(text: str) -> str | None:
	# Deteksi kategori dari teks pertanyaan user untuk filtering metadata.
	lower_text = text.lower()
	for key, normalized in KNOWN_CATEGORIES.items():
		if key in lower_text:
			return normalized
	return None


def category_filter(category: str) -> dict[str, Any]:
	# Bentuk filter Qdrant berbasis metadata category.
	return {
		"must": [
			{
				"key": "category",
				"match": {"value": category},
			}
		]
	}


def run_similarity_search(query: str, k: int = 5, category: str | None = None):
		# Retrieval utama RAG: semantic search dengan opsi filter category.
	if category:
		try:
			return qdrant.similarity_search(query, k=k, filter=category_filter(category))
		except Exception:
			# Fallback keeps app working if backend rejects filter shape.
			return qdrant.similarity_search(query, k=k)
	return qdrant.similarity_search(query, k=k)


def format_docs(docs, title: str | None = None) -> str:
		# Gabungkan dokumen retrieval menjadi teks konteks yang mudah dibaca LLM.
	if not docs:
		return "Tidak ada resume relevan yang ditemukan."

	parts = []
	if title:
		parts.append(title)

	for doc in docs:
		parts.append(doc.page_content)

	return "\n\n---\n\n".join(parts)


@tool
def search_resume(query: str) -> str:
	"""Cari resume relevan berdasarkan pertanyaan user. Otomatis gunakan filter category jika query menyebut kategori seperti IT, HR, Finance, dll."""
	# Tool utama untuk semua pertanyaan in-domain pada skenario demo.
	detected_category = extract_category_from_text(query)
	results = run_similarity_search(query, k=5, category=detected_category)
	if detected_category:
		return format_docs(results, title=f"[Filtered Category: {detected_category}]")
	return format_docs(results)


@tool
def shortlist_candidates(category: str, focus: str) -> str:
	"""Buat shortlist kandidat dari category tertentu. Gunakan tool ini ketika user minta rekomendasi per kategori. Input category contoh: IT, HR, Finance. Input focus contoh: python, data analyst, communication."""
	# Tool khusus saat user meminta shortlist kandidat berdasarkan kategori tertentu.
	normalized_category = KNOWN_CATEGORIES.get(category.lower(), category)
	results = run_similarity_search(focus, k=3, category=normalized_category)
	if not results:
		return f"Tidak ditemukan kandidat untuk category {normalized_category}."

	shortlist = [f"Shortlist untuk category {normalized_category} (focus: {focus}):"]
	for i, doc in enumerate(results, 1):
		# Snippet dipotong agar output ringkas saat tampil di chat.
		snippet = doc.page_content.replace("\n", " ")[:420]
		shortlist.append(f"{i}. {snippet}...")

	return "\n".join(shortlist)


# LLM reasoning layer untuk agent.
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.3)
# Agent ReAct: memilih kapan memanggil tools lalu menyusun jawaban final.
agent = create_react_agent(model=llm, tools=[search_resume, shortlist_candidates])

# System prompt sebagai guardrail agar jawaban tetap berbasis retrieval.
SYSTEM_PROMPT = """Kamu adalah asisten HR bernama ResumeBot.
Tugasmu membantu user mencari dan menganalisis resume dari vector database.

ATURAN:
1. Selalu gunakan tool search_resume sebelum menjawab.
2. Jika user meminta rekomendasi kandidat per kategori, gunakan tool shortlist_candidates.
3. Jawab berdasarkan hasil tool, jangan mengarang.
4. Jika data tidak ditemukan, katakan dengan jujur.
5. Jika pertanyaan di luar topik resume/karier, tolak dengan sopan.
6. Gunakan bahasa Indonesia yang ringkas dan jelas.
7. Jika ada konteks dari percakapan sebelumnya, gunakan chat history yang tersedia.
"""


def chat_agent(user_question: str, chat_history: list[dict]) -> dict:
	# Bangun urutan pesan: system -> riwayat pendek -> pertanyaan user terbaru.
	messages = [SystemMessage(content=SYSTEM_PROMPT)]

	# Keep at least the latest 3 turns (6 messages)
	for msg in chat_history[-6:]:
		if msg["role"] in ["Human", "user"]:
			messages.append(HumanMessage(content=msg["content"]))
		else:
			messages.append(AIMessage(content=msg["content"]))

	messages.append(HumanMessage(content=user_question))

	# Eksekusi agent (reasoning + tool calling) dalam satu invoke.
	result = agent.invoke({"messages": messages})
	answer = result["messages"][-1].content

	total_input_tokens = 0
	total_output_tokens = 0
	tool_messages = []

	# Ambil statistik token dan jejak tool untuk transparansi di UI.
	for message in result["messages"]:
		if hasattr(message, "response_metadata"):
			meta = message.response_metadata
			if "usage_metadata" in meta:
				total_input_tokens += meta["usage_metadata"].get("input_tokens", 0)
				total_output_tokens += meta["usage_metadata"].get("output_tokens", 0)
			elif "token_usage" in meta:
				total_input_tokens += meta["token_usage"].get("prompt_tokens", 0)
				total_output_tokens += meta["token_usage"].get("completion_tokens", 0)

		if isinstance(message, ToolMessage):
			tool_messages.append(str(message.content))

	# gpt-4o-mini pricing estimate in IDR, assuming IDR 17,000 per USD
	price_idr = 17_000 * (total_input_tokens * 0.15 + total_output_tokens * 0.6) / 1_000_000

	return {
		"answer": answer,
		"total_input_tokens": total_input_tokens,
		"total_output_tokens": total_output_tokens,
		"price_idr": price_idr,
		"tool_messages": tool_messages,
	}


# Konfigurasi halaman utama Streamlit.
st.set_page_config(
	page_title="ResumeBot - Resume RAG Assistant",
	page_icon="📄",
	layout="wide",
)

# Terapkan gaya visual custom untuk kebutuhan presentasi.
apply_custom_ui()

# Hero section: ringkasan produk yang ditampilkan di awal demo.
st.markdown(
	"""
	<div class="hero">
		<h1>ResumeBot Professional Workspace</h1>
		<p>Asisten rekrutmen berbasis RAG untuk menemukan kandidat yang relevan dari dataset resume dengan cepat, konsisten, dan dapat diaudit.</p>
		<div class="badge-row">
			<span class="badge">Qdrant Vector Search</span>
			<span class="badge">OpenAI GPT-4o-mini</span>
			<span class="badge">Collection: resumes</span>
		</div>
	</div>
	""",
	unsafe_allow_html=True,
)

# Status cards untuk menjelaskan komponen model, embedding, dan mode kerja.
status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:
	st.markdown(
		"""
		<div class="metric-card">
			<div class="metric-label">Model</div>
			<div class="metric-value">gpt-4o-mini</div>
		</div>
		""",
		unsafe_allow_html=True,
	)
with status_col2:
	st.markdown(
		"""
		<div class="metric-card">
			<div class="metric-label">Embedding</div>
			<div class="metric-value">text-embedding-3-small (1536)</div>
		</div>
		""",
		unsafe_allow_html=True,
	)
with status_col3:
	st.markdown(
		"""
		<div class="metric-card">
			<div class="metric-label">Mode</div>
			<div class="metric-value">Resume Retrieval</div>
		</div>
		""",
		unsafe_allow_html=True,
	)

with st.sidebar:
	# Sidebar berisi konteks penggunaan dan kontrol reset percakapan.
	st.header("Workspace")
	st.markdown(
		"""
<div class="sidebar-card">
ResumeBot membantu pencarian kandidat berdasarkan data resume.

Gunakan pertanyaan yang jelas: role, skill, level, dan konteks kebutuhan bisnis.
</div>
""",
		unsafe_allow_html=True,
	)

	st.markdown("### Contoh query")
	st.markdown(
		"""
- Cari kandidat kategori IT dengan skill Python
- Kandidat untuk posisi data analyst
- Ringkas profil kandidat untuk role HR
"""
	)

	if st.button("Reset Chat"):
		st.session_state.messages = []
		st.rerun()

	st.divider()
	st.caption("Collection aktif: resumes")

# Simpan histori chat lintas interaksi pengguna selama sesi aktif.
if "messages" not in st.session_state:
	st.session_state.messages = []

st.markdown("<div style='margin-top: 0.7rem;'></div>", unsafe_allow_html=True)

quick_col1, quick_col2, quick_col3 = st.columns(3)
quick_prompt = None
with quick_col1:
	# Tombol cepat untuk skenario demo kategori IT + Python.
	if st.button("Quick: IT Python", use_container_width=True):
		quick_prompt = "Carikan kandidat kategori IT yang memiliki skill Python dan jelaskan alasan kecocokan."
with quick_col2:
	# Tombol cepat untuk skenario demo role Data Analyst.
	if st.button("Quick: Data Analyst", use_container_width=True):
		quick_prompt = "Cari kandidat yang cocok untuk posisi Data Analyst dan rangkum skill utamanya."
with quick_col3:
	# Tombol cepat untuk skenario demo ringkasan kandidat HR.
	if st.button("Quick: HR Summary", use_container_width=True):
		quick_prompt = "Ringkas 3 kandidat terbaik untuk role HR dalam format poin."

# Render histori chat agar percakapan sebelumnya tetap terlihat (multi-turn).
for message in st.session_state.messages:
	display_role = "assistant"
	if message["role"] in ["Human", "user"]:
		display_role = "user"
	with st.chat_message(display_role):
		st.markdown(message["content"])

# Ambil prompt dari input chat atau quick prompt.
prompt = st.chat_input("Tanyakan kandidat yang kamu cari...")
if quick_prompt and not prompt:
	prompt = quick_prompt

if prompt:
	# Batasi context history agar efisien tapi tetap nyambung (3 turn terakhir).
	chat_history = st.session_state.messages[-6:]

	with st.chat_message("user"):
		st.markdown(prompt)
	st.session_state.messages.append({"role": "user", "content": prompt})

	with st.chat_message("assistant"):
		with st.spinner("Mencari resume relevan..."):
			try:
				# Jalankan pipeline RAG untuk menghasilkan jawaban berbasis dokumen.
				response = chat_agent(prompt, chat_history)
			except Exception as err:
				st.error(f"Terjadi error saat memproses query: {err}")
				st.stop()

		answer = response["answer"]
		st.markdown(answer)
		st.session_state.messages.append({"role": "assistant", "content": answer})

	# Bukti retrieval untuk kebutuhan auditability saat presentasi.
	if response["tool_messages"]:
		with st.expander("Dokumen yang diambil dari Vector DB", expanded=False):
			for i, doc in enumerate(response["tool_messages"], 1):
				st.text(f"[Dokumen {i}]\n{doc[:700]}...")

	# Transparansi biaya dan token usage untuk evaluasi performa model.
	with st.expander("Usage Details", expanded=False):
		col1, col2, col3 = st.columns(3)
		with col1:
			st.metric("Input Tokens", response["total_input_tokens"])
		with col2:
			st.metric("Output Tokens", response["total_output_tokens"])
		with col3:
			st.metric("Estimasi Biaya", f"Rp {response['price_idr']:.4f}")

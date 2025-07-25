# 🤖 Adaptive RAG Streamlit App

A Streamlit-based application that implements **Adaptive Retrieval-Augmented Generation (RAG)** with fallback mechanisms. The app answers user questions based on uploaded PDF documents using OpenAI's GPT-4.

---

## 🚀 Features

- 📤 Upload **multiple PDF files**
- 🧠 **Adaptive RAG**:
  - Detects query intent: `FACTUAL`, `PROCEDURAL`, or `REASONING`
  - Dynamically adjusts retrieval depth based on intent
- 🔄 **Fallback mechanisms**:
  - Rewrites vague queries
  - Increases context if retrieval is weak
  - Regenerates answer if initial output is short
- 🔐 **Secure OpenAI API key input** via Streamlit UI

---

## 🧩 Tech Stack

- Python 🐍
- Streamlit 🧪
- LangChain 🔗
- OpenAI GPT-4 🧠
- FAISS (vector database) 🧲

---

## 📦 Installation

1. **Clone the repository or copy files**
2. **Install dependencies**:

```bash
pip install streamlit langchain openai faiss-cpu PyPDF2
▶ How to Run

streamlit run adaptive_rag_app_ui_api_key.py
🔑 OpenAI API Key
You'll be prompted to enter your OpenAI API key in the app UI.

Get your API key from: https://platform.openai.com/account/api-keys

📁 Usage
Upload one or more PDF documents (e.g., product manuals, handbooks, etc.)

Enter your OpenAI API key

Ask natural language questions like:

"What is the warranty period?"

"How to reset the device?"

"Why is Model A better than Model B?"

✅ Query Intent Behavior
Intent	Meaning	Retrieval Depth
FACTUAL	Specific facts (e.g. dates)	2 chunks
PROCEDURAL	Steps / instructions	5 chunks
REASONING	Explanations, comparisons	8+ chunks

📌 Example
Query: "How do I connect this to Wi-Fi?"
Intent: PROCEDURAL
Answer: The device can be connected to Wi-Fi by navigating to...

🛡️ Security
Your API key is not stored or logged.

Entered key is used only during your session.


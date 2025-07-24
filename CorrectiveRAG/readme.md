Corrective RAG - Streamlit Educational Assistant

This Streamlit app demonstrates a full Corrective RAG (Retrieval-Augmented Generation) pipeline with:

Real vector search (FAISS)

Multi-topic knowledge base

Automatic LLM-based evaluation of retrieved context

Refined query correction and response regeneration

Full session logging and export

🔧 Features

📚 Selectable domains: General Science, Climate, Physics, Computer Science

🤖 LLM-powered evaluation of context: Relevance, Completeness, Accuracy, Specificity

🔁 Retry logic with auto-suggested refined query if initial context is poor

✅ Final response generated using corrected context

📥 CSV export of full query-context-evaluation-response log

📦 Requirements

Install the dependencies using pip:

pip install streamlit langchain openai chromadb faiss-cpu sentence-transformers pandas

Optional: Use a virtual environment for isolation.

python -m venv venv
venv\Scripts\activate      # For Windows
source venv/bin/activate    # For Mac/Linux

🚀 How to Run

Make sure you’re in the folder where your script is saved (e.g., corrective_rag_app.py) and run:

streamlit run corrective_rag_app.py

If you see streamlit: command not found, make sure:

You activated your virtual environment (if used)

streamlit is in your system PATH

🔐 OpenAI API Key

This app uses OpenAI's GPT (e.g., gpt-3.5-turbo) to evaluate and generate responses.

You will be prompted to paste your API key in the Streamlit sidebar. If you don’t have one:

Go to https://platform.openai.com/account/api-keys

Generate a new key and paste it into the app

📁 File Structure

project/
├── corrective_rag_app.py       # Main Streamlit app
├── README.md                   # This file

📝 Example Query

Query: "How does climate change affect sea levels?"

Retrieved Context: (general info on climate only)

Evaluation: Relevance: 0.4, Specificity: 0.2 → Action Needed: Yes

Refined Query: "climate change sea level rise effects glaciers thermal expansion"

Final Answer:

Climate change causes sea level rise due to melting glaciers and thermal expansion of oceans, threatening coastal habitats.

📈 Want to Improve Further?

Add file upload to build custom KBs

Use persistent vector stores (e.g., Pinecone, Qdrant)

Add scoring trend charts across sessions

Deploy to Streamlit Cloud

📬 Support

For help or suggestions, contact the developer or open an issue on your code repository if using version control.
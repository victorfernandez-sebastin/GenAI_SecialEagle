import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
import tempfile
import os

st.set_page_config(page_title="Adaptive RAG App", layout="centered")
st.title("📚 Adaptive RAG – AI Q&A over PDFs")

# === Step 0: Ask for OpenAI API Key ===
openai_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

if openai_key:
    # === Load LLM and Chains (with key) ===
    llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_key)
    embedding = OpenAIEmbeddings(openai_api_key=openai_key)

    intent_prompt = PromptTemplate.from_template("""
    Classify the user query into one of these categories:
    - FACTUAL
    - PROCEDURAL
    - REASONING

    Query: "{query}"
    Respond with just one word: FACTUAL, PROCEDURAL, or REASONING.
    """)
    intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

    rewrite_prompt = PromptTemplate.from_template("""
    The user asked a vague or unclear question:
    "{question}"

    Rewrite it to make it more specific for document search.
    """)
    rewrite_chain = LLMChain(llm=llm, prompt=rewrite_prompt)

    # === Helper Functions ===
    def load_and_split_pdfs(uploaded_files):
        documents = []
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            loader = PyPDFLoader(tmp_file_path)
            documents.extend(loader.load())
            os.remove(tmp_file_path)

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(documents)

    def adaptive_rag(query, retriever):
        if len(query.split()) < 4:
            st.warning("Query too short. Rewriting...")
            query = rewrite_chain.run(question=query)

        intent = intent_chain.run(query=query).strip().upper()
        st.info(f"🧠 Detected Query Type: **{intent}**")

        k = {"FACTUAL": 2, "PROCEDURAL": 5, "REASONING": 8}.get(intent, 4)
        docs = retriever.get_relevant_documents(query)

        if len(docs) < k:
            st.warning("Low context found. Expanding search...")
            k = k + 3
            docs = retriever.vectorstore.similarity_search(query, k=k)

        qa_chain = load_qa_chain(llm, chain_type="stuff")
        answer = qa_chain.run(input_documents=docs, question=query)

        if len(answer.strip()) < 20:
            st.warning("Weak answer. Regenerating...")
            more_docs = retriever.vectorstore.similarity_search(query, k=k + 3)
            answer = qa_chain.run(input_documents=more_docs, question=query)

        return answer

    # === File Upload ===
    uploaded_files = st.file_uploader("Upload one or more PDFs", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        with st.spinner("Loading and processing..."):
            chunks = load_and_split_pdfs(uploaded_files)
            vectorstore = FAISS.from_documents(chunks, embedding)
            retriever = vectorstore.as_retriever()

        st.success("✅ PDFs processed. Ask your question below:")

        query = st.text_input("🔍 Ask your question")
        if query:
            with st.spinner("Thinking..."):
                result = adaptive_rag(query, retriever)
            st.markdown("### ✅ Answer")
            st.success(result)

    else:
        st.info("Upload one or more PDF files to begin.")
else:
    st.warning("🔐 Please enter your OpenAI API key above to continue.")

import streamlit as st
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

# --- Session Log ---
if "log" not in st.session_state:
    st.session_state.log = []

if st.button("🔄 Clear / Start Over"):
    st.session_state.clear()
    st.rerun()

# --- Sidebar ---
st.sidebar.title("🔐 OpenAI Settings")
openai_api_key = st.sidebar.text_input("Enter OpenAI API key", type="password")

st.sidebar.title("📂 Knowledge Base")
topic = st.sidebar.selectbox("Choose Topic", ["General Science", "Climate", "Physics", "Computer Science"])

# --- Load Documents by Topic ---
kb = {
    "General Science": [
        {"q": "What is photosynthesis?", "a": "Photosynthesis is the process by which plants make food using sunlight."},
        {"q": "Define gravity.", "a": "Gravity is the force that attracts objects towards each other."},
    ],
    "Climate": [
        {"q": "What causes sea level rise?", "a": "Melting glaciers and thermal expansion of seawater due to climate change."},
        {"q": "Effects of climate change on oceans?", "a": "Leads to warmer oceans, sea level rise, and ocean acidification."}
    ],
    "Physics": [
        {"q": "Newton's second law?", "a": "Force equals mass times acceleration (F = ma)."},
        {"q": "What is energy?", "a": "Energy is the capacity to do work."},
    ],
    "Computer Science": [
        {"q": "Define overfitting in ML.", "a": "Overfitting occurs when a model memorizes training data and performs poorly on unseen data."},
        {"q": "What is an algorithm?", "a": "A step-by-step procedure to solve a problem or perform a task."},
    ]
}

# Vector DB Setup (FAISS)
documents = [Document(page_content=f"Q: {x['q']} A: {x['a']}", metadata={"topic": topic}) for x in kb[topic]]
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",model_kwargs={"device": "cpu"})
vectordb = FAISS.from_documents(documents, embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})

# --- Main App ---
st.title("📘 Corrective RAG - Educational QA Assistant")

if not openai_api_key:
    st.warning("Please enter OpenAI API key to proceed.")
else:
    llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model="gpt-3.5-turbo")

    query = st.text_input("Ask a question:", placeholder="e.g. How does climate change affect sea levels?")

    if query:
        context_docs = retriever.get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in context_docs]) or "No relevant context found."

        st.subheader("📄 Initial Retrieved Context")
        st.markdown(f"**Query:** {query}")
        st.markdown(f"**Context:**\n\n{context}")

        # Auto Evaluation Prompt
        eval_prompt = PromptTemplate(
            input_variables=["practice_query", "practice_context"],
            template="""
Evaluate the retrieved context against the query:

Query: {practice_query}
Context: {practice_context}

EVALUATE_CONTEXT:
- Relevance Score (0-1):
- Completeness Score (0-1):
- Accuracy Score (0-1):
- Specificity Score (0-1):
- Overall Quality: GOOD or POOR
- Action Needed: Yes/No
- Refined Query (if needed):
- Reasoning:
"""
        )

        filled_prompt = eval_prompt.format(practice_query=query, practice_context=context)

        if st.button("🤖 Auto Evaluate & Respond"):
            eval_result = llm.predict(filled_prompt)
            st.subheader("📊 Auto Evaluation Result")
            st.text_area("Evaluation:", value=eval_result, height=300)

            # Extract refined query or use original
            if "Refined Query" in eval_result and ":" in eval_result:
                lines = eval_result.splitlines()
                refined_line = [line for line in lines if "Refined Query" in line]
                refined_query = refined_line[0].split(":", 1)[1].strip() if refined_line else query
            else:
                refined_query = query

            # Generate Final Answer
            new_docs = retriever.get_relevant_documents(refined_query)
            new_context = "\n".join([doc.page_content for doc in new_docs])

            answer_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""
You are a helpful tutor. Use the context below to answer the question clearly.

Context:
{context}

Question:
{question}

Answer:
"""
            ).format(context=new_context, question=refined_query)

            final_answer = llm.predict(answer_prompt)

            st.subheader("✅ Final Response")
            st.markdown(final_answer)

            # Log the session
            st.session_state.log.append({
                "Topic": topic,
                "Query": query,
                "Initial Context": context,
                "Auto Evaluation": eval_result,
                "Refined Query": refined_query,
                "Final Context": new_context,
                "Final Answer": final_answer
            })

    # --- Download Logs ---
    if st.session_state.log:
        st.subheader("📋 Session Logs")
        df = pd.DataFrame(st.session_state.log)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Log", data=csv, file_name="rag_session_log.csv", mime="text/csv")

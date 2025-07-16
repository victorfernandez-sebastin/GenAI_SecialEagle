import os
from dotenv import load_dotenv
import streamlit as st

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# --- 0. Streamlit Page Configuration ---
st.set_page_config(
    page_title="Website Q&A with LangChain",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Ask Me Anything from a Website!")
st.markdown("Enter a website URL and ask questions about its content. Powered by LangChain and OpenAI.")

# --- 1. Secure Configuration (API Key Loading) ---
# Load environment variables from .env file
load_dotenv()

# Get API key and User-Agent from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USER_AGENT = os.getenv("USER_AGENT")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("Configuration")
    st.markdown("API Key is loaded from your local `.env` file for security.")

    if not OPENAI_API_KEY:
        st.error("OPENAI_API_KEY not found in environment variables.")
        st.info("Please create a `.env` file in the same directory as this script and add `OPENAI_API_KEY=\"your_api_key_here\"`")
        st.stop() # Stop execution if API key is missing

    # Optional: Display a warning if USER_AGENT is not set
    if not USER_AGENT:
        st.warning("USER_AGENT environment variable not set. It's recommended to set it in your `.env` file for reliable web scraping.")
        st.markdown("Example: `USER_AGENT=\"MyLangChainApp/1.0 (contact@example.com)\"`")
    else:
        # Set the environment variable for WebBaseLoader
        os.environ["USER_AGENT"] = USER_AGENT

    st.subheader("Website URL")
    website_url = st.text_input(
        "Enter the URL of the website you want to query:",
        "https://www.jovintech.in/#[object%20Object]" # Default URL
    )

    st.markdown("---")
    st.info("💡 **Tip:** Clear cache if you change the URL to re-process content.")
    if st.button("Clear Cache"):
        st.cache_resource.clear()
        st.success("Cache cleared!")
        st.rerun() # Rerun the app to re-process with new URL (if entered)

# --- Define Caching for Expensive Operations ---
@st.cache_resource(show_spinner="Loading and processing website content...")
def load_and_process_website(url: str, api_key: str):
    """
    Loads website content, splits it into chunks, creates embeddings,
    and stores them in a vector database. Caches the result.
    """
    if not url:
        return None, None

    try:
        # Set the OpenAI API key for LangChain's models globally
        os.environ["OPENAI_API_KEY"] = api_key

        st.write(f"Loading content from: {url}")
        loader = WebBaseLoader(url)
        docs = loader.load()
        st.write(f"Loaded {len(docs)} document(s).")

        st.write("Splitting documents into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_documents(docs)
        st.write(f"Split into {len(chunks)} chunks.")

        st.write("Creating embeddings and storing in vector database (ChromaDB)...")
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(chunks, embeddings)
        st.write("Vector database created.")

        return vectorstore

    except Exception as e:
        st.error(f"Failed to load or process website: {e}")
        st.stop()
        return None


# --- Load and Process Website Content ---
# This function will only run once and cache its results
vectorstore = load_and_process_website(website_url, OPENAI_API_KEY)

if vectorstore:
    # --- 5. Set up the Retriever ---
    retriever = vectorstore.as_retriever()

    # --- 6. Define the LLM and Prompt Template ---
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

    qa_template = """Use the following pieces of context to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    ----------------
    {context}
    ----------------
    Question: {question}
    Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(qa_template)

    # --- 7. Create the RetrievalQA Chain ---
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    # --- 8. Interact with the LLM Application (UI) ---
    st.subheader("Ask a Question")
    user_question = st.text_area(
        "Enter your question about the website content here:",
        placeholder="e.g., What is this article about?",
        height=100
    )

    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    response = qa_chain.invoke({"query": user_question})
                    st.success("Answer:")
                    st.write(response['result'])

                    if 'source_documents' in response and response['source_documents']:
                        st.subheader("Sources Used:")
                        for i, doc in enumerate(response['source_documents']):
                            st.markdown(f"**Source {i+1}:** {doc.metadata.get('source', 'N/A')}")
                            st.markdown(f"Snippet: *{doc.page_content[:300]}...*")
                            st.markdown("---")

                except Exception as e:
                    st.error(f"An error occurred while getting the answer: {e}")
                    st.info("Please check your OpenAI API key and network connection.")
        else:
            st.warning("Please enter a question to get an answer.")
else:
    st.info("Please enter a valid website URL in the sidebar to begin.")
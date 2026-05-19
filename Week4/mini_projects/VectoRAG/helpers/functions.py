import os
import streamlit as st
from helpers.classes import JinaEmbeddings
from langchain_groq import ChatGroq
from qdrant_client.models import Distance, VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from pathlib import Path
import tempfile
from langchain_qdrant import QdrantVectorStore


COLLECTION_NAME = "rag_temp_collection"


def load_file(uploaded_file) -> list:
    suffix = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
        elif suffix == ".txt":
            loader = TextLoader(tmp_path, encoding="utf-8")
        else:
            st.error(f"Unsupported file type: {suffix}")
            return []
        docs = loader.load()
    finally:
        os.unlink(tmp_path)
    return docs

def get_vectorstore():
    embeddings = get_embeddings()
    return QdrantVectorStore(
        client=st.session_state.qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

def clear_db():
    client = st.session_state.qdrant_client
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
    st.session_state.collection_ready = False
    st.session_state.messages = []
    st.session_state.doc_count = 0


def ingest_docs(docs: list):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()
    client = st.session_state.qdrant_client

    # Create/recreate collection
    sample_emb = embeddings.embed_query("test")
    dim = len(sample_emb)

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    vectorstore.add_documents(chunks)
    return len(chunks)

def get_embeddings():
    jina_key = os.getenv("JINA_API_KEY", "")
    if not jina_key:
        st.error("JINA_API_KEY not found in .env")
        st.stop()
    return JinaEmbeddings(api_key=jina_key)

def get_llm():
    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key:
        st.error("GROQ_API_KEY not found in .env")
        st.stop()
    return ChatGroq(api_key=groq_key, model_name="llama-3.3-70b-versatile", temperature=0.3)


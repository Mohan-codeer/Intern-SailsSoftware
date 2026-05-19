import streamlit as st
from helpers.functions import *
from static.frontend import *
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="VectoRAG",
    page_icon="⬜️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient



if "qdrant_client" not in st.session_state:
    st.session_state.qdrant_client = QdrantClient(host="localhost", port=6333)
if "collection_ready" not in st.session_state:
    st.session_state.collection_ready = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0


st.markdown(css, unsafe_allow_html=True)


with st.sidebar:
    st.markdown(sidebar, unsafe_allow_html=True)

    st.markdown(sidebar_txt, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if st.button("⬡ Vectorize & Ingest", use_container_width=True):
        if not uploaded_files:
            st.warning("Upload at least one file first.")
        else:
            all_docs = []
            with st.spinner("Loading documents…"):
                for f in uploaded_files:
                    docs = load_file(f)
                    all_docs.extend(docs)

            if all_docs:
                with st.spinner("Embedding with Jina AI…"):
                    n_chunks = ingest_docs(all_docs)
                st.session_state.collection_ready = True
                st.session_state.doc_count += n_chunks
                st.success(f"✓ {n_chunks} chunks indexed from {len(uploaded_files)} file(s)")

    st.markdown(div_style, unsafe_allow_html=True)

    if st.session_state.collection_ready:
        st.markdown(session_state(st.session_state.doc_count, len(st.session_state.messages)//2), unsafe_allow_html=True)

    st.markdown(database_side, unsafe_allow_html=True)
    with st.container():
        st.markdown(danger_button, unsafe_allow_html=True)
        if st.button("✕ Clear DB", use_container_width=True):
            clear_db()
            st.success("Database cleared.")
            st.rerun()
        st.markdown(div, unsafe_allow_html=True)

    st.markdown(jina_css, unsafe_allow_html=True)


st.markdown(main, unsafe_allow_html=True)

if st.session_state.collection_ready:
    st.markdown(status_pill_ready, unsafe_allow_html=True)
else:
    st.markdown(status_pill_unready, unsafe_allow_html=True)

chat_html = chat_container
if not st.session_state.messages:
    chat_html += chat_css
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += state_user(True, msg["content"])
        else:
            chat_html += state_user(False, msg["content"])
chat_html += div
st.markdown(chat_html, unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    query = st.text_input("Ask a question…", key="query_input", label_visibility="collapsed",
                          placeholder="Ask anything about your documents…")
with col_btn:
    send = st.button("Ask →", use_container_width=True)

if send and query:
    if not st.session_state.collection_ready:
        st.warning("Please upload and vectorize documents first.")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.spinner("Thinking…"):
            try:
                vs = get_vectorstore()
                llm = get_llm()
                retriever = vs.as_retriever(search_kwargs={"k": 4})

                prompt = ChatPromptTemplate.from_template(
                    "Use the following context to answer the question.\n\n"
                    "Context:\n{context}\n\n"
                    "Question: {question}\n\n"
                    "Answer concisely and accurately based only on the context."
                )

                chain = (
                    {"context": retriever, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                )
                answer = chain.invoke(query)
            except Exception as e:
                answer = f"Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

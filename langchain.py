import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
 
load_dotenv()

st.set_page_config(page_title="Groq AI Chat with LangChain")
st.title("LangChain + Groq Chat")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = llm.invoke(st.session_state.messages)
        st.markdown(response.content)
    
    st.session_state.messages.append(AIMessage(content=response.content))

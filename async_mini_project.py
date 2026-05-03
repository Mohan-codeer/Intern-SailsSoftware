import streamlit as st
from langchain_groq import ChatGroq
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

st.title("chat models") 

if "left_content" not in st.session_state:
    st.session_state.left_content = []
if "right_content" not in st.session_state:
    st.session_state.right_content = []

async def sync_ai_call(placeholder):
    llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"))
    
    res = await llm.ainvoke("What is 1+1?")
    st.session_state.left_content.append(f"Sync: {res.content}")
    with placeholder:
        for m in st.session_state.left_content: st.write(m)
    
    await asyncio.sleep(3)

async def async_ai_call(placeholder):
    llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"))
    
    res = await llm.ainvoke("What is 1+1?")
    await asyncio.sleep(3)
    st.session_state.right_content.append(f"Async: {res.content}")
    with placeholder:
        for m in st.session_state.right_content: st.write(m)

async def main():
    c1, c2 = st.columns(2)
    
    out_l, out_r = st.columns(2)
    left_placeholder = out_l.container()
    right_placeholder = out_r.container()

    if c1.button("Start Sync Process", use_container_width=True):
        st.session_state.left_content = []
        await sync_ai_call(left_placeholder)
        
    if c2.button("Start Async Process", use_container_width=True):
        st.session_state.right_content = []
        await async_ai_call(right_placeholder)

    with left_placeholder:
        for m in st.session_state.left_content: st.write(m)
    with right_placeholder:
        for m in st.session_state.right_content: st.write(m)

if __name__ == "__main__":
    asyncio.run(main())
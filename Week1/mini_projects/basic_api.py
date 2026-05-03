import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

load_dotenv()

st.title("Chat")

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

if "msgs" not in st.session_state:
    st.session_state.msgs = []


for m in st.session_state.msgs:

    if m["role"] == "user":
        label = "You"
    else:
        label = "AI"
    
    st.markdown(f"{label}: {m['content']}")

text = st.chat_input("Type")

if text is not None:
    user_message = {"role": "user", "content": text}
    st.session_state.msgs.append(user_message)
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=st.session_state.msgs
    )
    
    ai_content = response.choices[0].message.content
    
    ai_message = {"role": "assistant", "content": ai_content}
    st.session_state.msgs.append(ai_message)
    
    st.rerun()

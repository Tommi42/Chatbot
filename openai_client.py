import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()

def get_response():
    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages= st.session_state.message_list,
        stream=True,
    )
    return stream

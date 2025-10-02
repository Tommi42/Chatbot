from langchain_core.messages.utils import MessageLikeRepresentation
from openai.types.chat.completion_create_params import ResponseFormat
import streamlit as st
from openai_client import get_response
from openai_client import message_manager, init_chat_model_langchain, display_message
from openai_client import Role
import os

if "chat_model" not in st.session_state or "message_list" not in st.session_state:
    init_chat_model_langchain()

st.set_page_config(page_title="Chatbot", layout="wide")

c1, c2 = st.columns([5, 1])

input = st.chat_input("Type your message here")


with c2:
    st.subheader("About")
    st.text(
        "This is a Demo Chatbot built using Streamlit as UI and langchain as backend to manage LLM."
    )
    st.markdown("This project was built from ME, *Tommaso Cambursano* :)")
    st.text(
        "It is just a demo to demonstrate my knoledge on Langchain and LLM managing. You can directly ask the chatbot about me and me previuos project."
    )

    st.button("New chat", on_click=lambda: st.session_state.message_list.clear())


with c1:
    st.title("Chatbot")

    for message in st.session_state.message_list:
        display_message(message)

    if input:
        with st.chat_message("user"):
            st.write(input)
        message_manager(Role("user"), input)

        response = get_response()

        with st.chat_message("assistant"):
            response_txt = st.write_stream(response)

        message_manager(Role("assistant"), str(response_txt))

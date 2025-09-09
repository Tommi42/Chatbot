import streamlit as st
from openai_client import get_response
import os

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

st.title("Chatbot")

input = st.chat_input("Type your message here")

for message in st.session_state.message_list:
    if message['role'] == 'user':
        st.chat_message("user").markdown(message['content'])
    elif message['role'] == 'assistant':
        st.chat_message("assistant").markdown(message['content'])

if input:
    with st.chat_message("user"):
        st.write(input)
    st.session_state.message_list.append({"role": "user", "content": input})
    response = get_response()
    print(response)
    with st.chat_message("assistant"):
        response_txt = st.write_stream(response)
    st.session_state.message_list.append({"role": "assistant", "content": response_txt})

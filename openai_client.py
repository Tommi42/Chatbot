from socket import AI_ADDRCONFIG
from sqlalchemy.sql.roles import ReturnsRowsRole
import streamlit as st
import openai
from dotenv import load_dotenv
from enum import Enum
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()


class Role(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


def get_response():
    chat_model = st.session_state.chat_model

    stream = chat_model.stream(
        input=st.session_state.message_list,
        stream=True,
    )
    return stream


def init_chat_model_langchain():
    try:
        prompt = open("initial_prompt.txt", "r").read()
    except FileNotFoundError:
        prompt = ""
    st.session_state.message_list = [SystemMessage(content=prompt)]

    st.session_state.chat_model = init_chat_model(
        "gpt-4o", model_provider="openai", temperature=0
    )

    return True


def message_manager(role: Role, content: str):
    if role == Role.USER:
        message = HumanMessage(content=content)
    elif role == Role.SYSTEM:
        message = SystemMessage(content=content)
    elif role == Role.ASSISTANT:
        message = AIMessage(content=content)
    else:
        raise ValueError("Invalid role")

    st.session_state.message_list.append(message)
    return message


def display_message(message):
    if isinstance(message, HumanMessage):
        st.chat_message("user").markdown(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").markdown(message.content)
    else:
        pass  # Do not diplay anaything else

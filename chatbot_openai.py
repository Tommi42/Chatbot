import streamlit as st
import openai
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Chatbot with OpenAI",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 AI Chatbot powered by OpenAI")
st.markdown("Un chatbot intelligente che utilizza GPT per conversazioni naturali!")

# Sidebar for API key input
with st.sidebar:
    st.header("🔑 Configurazione")

    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Inserisci la tua API key di OpenAI. Puoi ottenerla da https://platform.openai.com/api-keys"
    )

    if api_key:
        openai.api_key = api_key
        st.success("✅ API Key configurata!")
    else:
        st.warning("⚠️ Inserisci la tua API Key per iniziare")

    st.markdown("---")

    # Model selection
    model = st.selectbox(
        "Modello GPT",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
        index=0,
        help="Scegli il modello GPT da utilizzare"
    )

    # Temperature setting
    temperature = st.slider(
        "Creatività (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Più alto = più creativo, più basso = più preciso"
    )

    # Max tokens
    max_tokens = st.slider(
        "Lunghezza massima risposta",
        min_value=50,
        max_value=2000,
        value=500,
        step=50,
        help="Numero massimo di token per la risposta"
    )

    st.markdown("---")

    # System prompt customization
    st.subheader("🎭 Personalità del Bot")
    system_prompt = st.text_area(
        "Prompt di sistema",
        value="Sei un assistente utile, amichevole e intelligente che risponde in italiano. Sei sempre cortese e cerca di essere il più utile possibile.",
        height=100,
        help="Definisce la personalità e il comportamento del chatbot"
    )

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Cancella Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"🕐 {message['timestamp']}")

def get_openai_response(messages, model, temperature, max_tokens):
    """Get response from OpenAI API"""
    try:
        client = openai.OpenAI(api_key=openai.api_key)

        # Prepare messages for OpenAI API
        api_messages = [{"role": "system", "content": system_prompt}]

        # Add chat history (limit to last 10 messages to avoid token limits)
        for msg in messages[-10:]:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )

        return response.choices[0].message.content

    except openai.AuthenticationError:
        return "❌ Errore di autenticazione: Verifica che la tua API key sia corretta."
    except openai.RateLimitError:
        return "⚠️ Limite di velocità raggiunto: Troppo molte richieste. Riprova tra un momento."
    except openai.InvalidRequestError as e:
        return f"❌ Richiesta non valida: {str(e)}"
    except Exception as e:
        return f"❌ Errore imprevisto: {str(e)}"

# Main chat interface
if not api_key:
    st.info("👈 Inserisci la tua API Key OpenAI nella barra laterale per iniziare!")
else:
    # Accept user input
    if prompt := st.chat_input("Scrivi il tuo messaggio..."):
        # Get current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"🕐 {timestamp}")

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = get_openai_response(
                    st.session_state.messages,
                    model,
                    temperature,
                    max_tokens
                )

            st.markdown(response)

            # Add timestamp
            response_timestamp = datetime.now().strftime("%H:%M:%S")
            st.caption(f"🕐 {response_timestamp}")

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": response_timestamp
        })

# Footer with usage stats
if api_key and st.session_state.messages:
    with st.expander("📊 Statistiche conversazione"):
        user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
        bot_messages = len([msg for msg in st.session_state.messages if msg["role"] == "assistant"])
        total_chars = sum(len(msg["content"]) for msg in st.session_state.messages)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messaggi utente", user_messages)
        with col2:
            st.metric("Risposte bot", bot_messages)
        with col3:
            st.metric("Caratteri totali", total_chars)

        st.info(f"💡 **Suggerimento**: Stai usando il modello **{model}** con temperatura **{temperature}**")

# Warning about costs
if api_key:
    st.warning("""
    ⚠️ **Nota sui costi**: Questo chatbot utilizza le API a pagamento di OpenAI.
    Ogni messaggio comporta un costo in base al modello utilizzato e alla lunghezza della conversazione.
    Controlla sempre il tuo usage su [OpenAI Platform](https://platform.openai.com/usage).
    """)

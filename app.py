import streamlit as st
import openai
import os
from streamlit_option_menu import option_menu

# API-Key aus Umgebungsvariable laden
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")

# Custom CSS im Stil von lovable.dev
st.markdown("""
<style>
body {
    background-color: #0d0d0d;
    font-family: 'Lexend', sans-serif;
    color: #f2f2f2;
}
input, textarea {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}
.stButton > button {
    background-color: #1f1f1f;
    color: #ffffff;
    border-radius: 50px;
    padding: 0.5rem 1rem;
    border: none;
    transition: 0.2s ease;
}
.stButton > button:hover {
    background-color: #333;
}
.sidebar .sidebar-content {
    background-color: #0d0d0d;
}
.stTextInput > div > div > input {
    padding: 0.75rem;
    font-size: 16px;
}
.chat-bubble {
    padding: 0.75rem;
    margin: 0.5rem 0;
    background-color: #1a1a1a;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Chatverlauf initialisieren
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Menü Toggle oben links
with st.container():
    with st.expander("≡ Menü", expanded=False):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.button("👤\nProfil")
        with col2:
            st.button("★\nGespeichert")
        with col3:
            st.button("📅\nKalender")
        with col4:
            st.button("💬\nNachrichten")
        with col5:
            st.button("!\nFeedback")
        with col6:
            st.button("?\nHilfe")

# Titelbereich
st.markdown("<h1 style='text-align: center;'>Hallo, wie kann ich dir helfen?</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Dies ist ein funktionaler MVP mit optischen Platzhaltern.</p>", unsafe_allow_html=True)

# Chat-Ausgabe
for user_input, response in st.session_state.chat_history:
    st.markdown(f"<div class='chat-bubble'><strong>Du:</strong> {user_input}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble'><strong>CORE:</strong> {response}</div>", unsafe_allow_html=True)

# Eingabefeld unten zentriert
with st.container():
    st.markdown("<div style='position: fixed; bottom: 2rem; left: 0; right: 0; margin: auto; width: 60%;'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([0.1, 0.7, 0.1, 0.1])
    with col1:
        st.button("🎤")  # Spracheingabe (optisch)
    with col2:
        user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed")
    with col3:
        st.button("⋯")  # Upload Button (optisch)
    with col4:
        if st.session_state.get("awaiting_response", False):
            if st.button("⏹️"):
                st.session_state.awaiting_response = False
        else:
            if st.button("⬆️") and user_input:
                try:
                    st.session_state.awaiting_response = True
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": user_input}]
                    )
                    answer = response.choices[0].message.content
                except Exception as e:
                    answer = f"[Fehler bei GPT]: {e}"
                st.session_state.chat_history.append((user_input, answer))
                st.session_state.awaiting_response = False
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

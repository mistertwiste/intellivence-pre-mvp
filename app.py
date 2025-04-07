import streamlit as st
from PIL import Image
from utils import optimize_prompt, ask_gpt
from streamlit_extras.switch_page_button import switch_page
import base64

# Seiteneinstellungen
st.set_page_config(page_title="CORE Pre-MVP", page_icon="🤖", layout="wide")

# CSS für globale Schriftart und optische Anpassungen
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Lexend', sans-serif;
    }

    .chat-entry {
        border-radius: 12px;
        padding: 8px;
        margin: 6px 0;
        background-color: #1e1e1e;
    }

    .icon-button {
        background-color: #262730;
        border: none;
        border-radius: 6px;
        padding: 6px;
        margin: 2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State initialisieren
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# Menüleiste (von oben nach unten)
with st.expander("☰ Menü", expanded=False):
    cols = st.columns(6)
    with cols[0]:
        st.link_button("🧑 Profil", "#", type="secondary")
    with cols[1]:
        st.link_button("⭐ Gespeichert", "#", type="secondary")
    with cols[2]:
        st.link_button("📅 Kalender", "#", type="secondary")
    with cols[3]:
        st.link_button("💬 Nachrichten", "#", type="secondary")
    with cols[4]:
        st.link_button("❗ Feedback", "#", type="secondary")
    with cols[5]:
        st.link_button("❓ Hilfe", "#", type="secondary")

# Titel und Untertitel
st.markdown("""
    <h1 style='text-align: center;'>Hallo, wie kann ich dir helfen?</h1>
    <p style='text-align: center;'>Dies ist ein funktionaler MVP mit optischen Platzhaltern.</p>
""", unsafe_allow_html=True)

# Chatverlauf anzeigen
for entry in st.session_state.chat_history:
    st.markdown(f"<div class='chat-entry'><strong>Du:</strong> {entry['user']}<br><strong>CORE:</strong> {entry['gpt']}</div>", unsafe_allow_html=True)

st.markdown("""<br><br><br><br><br><br>""")

# Eingabezeile unten zentriert
with st.container():
    col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
    with col1:
        st.button("🎤", help="Spracheingabe (optisch)")
    with col2:
        user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed")
    with col3:
        if st.session_state.is_generating:
            stop = st.button("⏹️")
            if stop:
                st.session_state.is_generating = False
        else:
            send = st.button("➤")

# Verarbeiten der Eingabe
if user_input and not st.session_state.is_generating:
    st.session_state.is_generating = True
    optimized = optimize_prompt(user_input)
    try:
        gpt_response = ask_gpt(optimized)
    except Exception as e:
        gpt_response = f"[Fehler bei GPT]:\n{str(e)}"

    st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
    st.experimental_rerun()

# Hinweis auf Teststatus
st.markdown("""<br><sub>⚠️ Dies ist ein MVP. Viele Elemente sind rein visuell.</sub>""")

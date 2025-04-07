import streamlit as st
from openai import OpenAI

# Seiteneinstellungen
st.set_page_config(page_title="Hallo", layout="wide")

# Styles
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Lexend', sans-serif;
        }
        .chat-text {
            font-family: monospace;
        }
        .bottom-bar {
            position: fixed;
            bottom: 1.5rem;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            background-color: #1f1f1f;
            padding: 0.5rem;
            border-radius: 8px;
        }
        .bottom-bar input {
            flex-grow: 1;
            height: 36px;
            border-radius: 6px;
            padding: 0 10px;
            border: none;
            background-color: #2c2c2c;
            color: white;
        }
        .bottom-button {
            background-color: #444;
            border: none;
            padding: 0.5rem 0.8rem;
            border-radius: 6px;
            color: white;
            font-size: 18px;
        }
        .top-menu {
            position: fixed;
            top: 0.5rem;
            left: 0.5rem;
            background-color: #1e1e1e;
            padding: 0.7rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            z-index: 10;
        }
        .top-menu-toggle {
            position: fixed;
            top: 0.5rem;
            left: 0.5rem;
            z-index: 11;
            background-color: #333;
            padding: 0.4rem 0.6rem;
            border-radius: 6px;
            color: white;
            font-size: 18px;
            border: none;
        }
        .top-menu button {
            display: block;
            width: 100%;
            margin-bottom: 0.5rem;
            text-align: left;
            background: none;
            border: none;
            color: white;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Init OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session States
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

# Menü Toggle Button
if st.button("≡", key="menu_toggle", help="Menü öffnen"):
    st.session_state.menu_open = not st.session_state.menu_open

# Menü Dropdown oben
if st.session_state.menu_open:
    st.markdown("""
        <div class='top-menu'>
            <button>👤 Profil</button>
            <button>★ Gespeichert</button>
            <button>📅 Kalender</button>
            <button>✉ Nachrichten</button>
            <button>! Feedback</button>
            <button>? Hilfe</button>
        </div>
    """, unsafe_allow_html=True)

# Haupttitel
st.markdown("# Hallo, wie kann ich dir helfen?")

# Chatverlauf anzeigen
for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-text'><strong>CORE:</strong> {entry['gpt']}</div>", unsafe_allow_html=True)

# Fixierte Eingabezeile unten
st.markdown("""
<div class="bottom-bar">
    <button class="bottom-button" disabled>🎤</button>
    <input name="user_input" placeholder="Schreib etwas..." />
    <button class="bottom-button" disabled>...</button>
</div>
""", unsafe_allow_html=True)

# Eingabeverarbeitung
user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed")
if st.button("⏎ Senden", key="send") and user_input:
    optimized = optimize_prompt(user_input)
    gpt_response = ask_gpt(optimized)
    st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
    st.rerun()

if st.session_state.awaiting_response:
    if st.button("⏹ Stopp", key="stop"):
        st.stop()

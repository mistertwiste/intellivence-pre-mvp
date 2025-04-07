import streamlit as st
from openai import OpenAI

# Seiteneinstellungen
st.set_page_config(page_title="Hallo", layout="wide")

# Style & Schrift
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
        }
        .bottom-bar input {
            flex-grow: 1;
            height: 40px;
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
        .top-dropdown {
            position: fixed;
            top: 1rem;
            left: 1rem;
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .top-dropdown button {
            display: block;
            width: 100%;
            margin-bottom: 0.5rem;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# Init OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

# Menü-Toggle oben links
if st.button("≡", key="menu_toggle"):
    st.session_state.menu_open = not st.session_state.menu_open

# Manuelles Dropdown-Menü oben links
if st.session_state.menu_open:
    with st.container():
        st.markdown("""
            <div class='top-dropdown'>
        """, unsafe_allow_html=True)
        st.button("👤 Profil")
        st.button("★ Gespeichert")
        st.button("📅 Kalender")
        st.button("✉ Nachrichten")
        st.button("! Feedback")
        st.button("? Hilfe")
        st.markdown("""
            </div>
        """, unsafe_allow_html=True)

# Überschrift (ohne Unterzeile)
st.markdown("# Hallo, wie kann ich dir helfen?")

# Chatverlauf
for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-text'><strong>CORE:</strong> {entry['gpt']}</div>", unsafe_allow_html=True)

# Eingabe unten fixiert
st.markdown("""
<div class="bottom-bar">
    <button class="bottom-button" disabled>🎤</button>
    <form action="" method="post" style="flex-grow:1;">
        <input name="user_input" placeholder="Schreib etwas..." autocomplete="off" />
    </form>
    <button class="bottom-button" disabled>...</button>
</div>
""", unsafe_allow_html=True)

# Dynamischer Button (⏎ oder ⏹)
if st.session_state.awaiting_response:
    if st.button("⏹ Stopp", key="stop"):
        st.stop()
else:
    user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed", key="text")
    if st.button("⏎", key="send") and user_input:
        optimized = optimize_prompt(user_input)
        gpt_response = ask_gpt(optimized)
        st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
        st.rerun()

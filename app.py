import streamlit as st
from openai import OpenAI

# Page setup
st.set_page_config(page_title="Hallo", layout="wide")

# Fonts & Style
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Lexend', sans-serif;
        }
        .chat-text {
            font-family: monospace;
        }
        .input-row {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 2rem;
            gap: 0.5rem;
        }
        .input-box {
            width: 400px;
            height: 35px;
            border-radius: 6px;
            padding: 5px;
        }
        .top-button {
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 100;
        }
    </style>
""", unsafe_allow_html=True)

# Init OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session Init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False

# Optimizer

def optimize_prompt(user_input):
    return f"Optimierter Prompt: {user_input.strip().capitalize()}?"

# GPT-Kommunikation

def ask_gpt(optimized_prompt):
    st.session_state.awaiting_response = True
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": optimized_prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Fehler bei GPT]: {e}"
    finally:
        st.session_state.awaiting_response = False

# --- Dropdown-Menü oben links ---
menu_open = st.sidebar.toggle("≡ Menü", value=True)
if menu_open:
    st.sidebar.markdown("## Navigation")
    st.sidebar.button("👤 Profil")
    st.sidebar.button("★ Gespeichert")
    st.sidebar.button("📅 Kalender")
    st.sidebar.button("✉ Nachrichten")
    st.sidebar.button("! Feedback")
    st.sidebar.button("? Hilfe")

# --- Haupttitel ---
st.markdown("# Hallo, wie kann ich dir helfen?")
st.markdown("Dies ist ein funktionaler MVP mit optischen Platzhaltern.")

# --- Chatverlauf ---
for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-text'><strong>CORE:</strong> {entry['gpt']}</div>", unsafe_allow_html=True)

# --- Eingabefeld unten ---
st.markdown("""
    <div class="input-row">
        <button disabled>🎤</button>
        <form action="" method="post">
            <input name="user_input" class="input-box" placeholder="Schreib etwas...">
        </form>
""", unsafe_allow_html=True)

# Sende-/Stopp-Button
if st.session_state.awaiting_response:
    if st.button("⏹ Stopp"):
        st.stop()
else:
    user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed", key="textinput")
    if st.button("⏎ Senden") and user_input:
        optimized = optimize_prompt(user_input)
        gpt_response = ask_gpt(optimized)
        st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
        st.rerun()

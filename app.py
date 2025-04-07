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
            bottom: 2rem;
            left: 0;
            right: 0;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            padding: 0 2rem;
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
        .sidebar-icons button {
            width: 100%;
            text-align: left;
            margin-bottom: 1rem;
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

# Prompt-Optimierung

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

# Sidebar Menü (einfach, ohne Titel)
with st.sidebar:
    st.markdown("<div class='sidebar-icons'>", unsafe_allow_html=True)
    st.button("👤 Profil")
    st.button("★ Gespeichert")
    st.button("📅 Kalender")
    st.button("✉ Nachrichten")
    st.button("! Feedback")
    st.button("? Hilfe")
    st.markdown("</div>", unsafe_allow_html=True)

# Überschrift (keine Unterzeile mehr)
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
""", unsafe_allow_html=True)

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

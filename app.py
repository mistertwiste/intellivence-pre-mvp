import streamlit as st
from openai import OpenAI

# Layout & Seitenkonfiguration
st.set_page_config(page_title="Hallo", layout="wide")

# Schriftstil global setzen (außer im Chatbereich)
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Lexend', sans-serif;
        }
        .chat-text {
            font-family: monospace;
        }
    </style>
""", unsafe_allow_html=True)

# OpenAI Client initialisieren (API-Key über Secrets setzen)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Prompt-Optimierer (Platzhalter)
def optimize_prompt(user_input):
    return f"Optimierter Prompt: {user_input.strip().capitalize()}?"

# GPT-Anfrage

def ask_gpt(optimized_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": optimized_prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Fehler bei GPT]: {e}"

# --- Navigation oben (Dropdown Style) ---
with st.expander("≡ Menü", expanded=True):
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.button("👤")  # Profil
    with col2:
        st.button("+")  # Neuer Chat
    with col3:
        st.button("📅")  # Kalender
    with col4:
        st.button("★")  # Gespeichert
    with col5:
        st.button("✉")  # Nachrichten
    with col6:
        st.button("! ")  # Feedback
    with col7:
        st.button("?")  # Hilfe

# --- Überschrift / App Titel ---
st.markdown("# Hallo, wie kann ich dir helfen?")
st.markdown("Dies ist ein funktionaler MVP mit optischen Platzhaltern.")

# --- Chatverlauf ---
for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-text'><strong>CORE:</strong> {entry['gpt']}</div>", unsafe_allow_html=True)

# --- Eingabezeile (kompakter) ---
col1, col2, col3 = st.columns([0.1, 0.4, 0.1])
with col1:
    st.button("🎤")  # Spracheingabe (optisch)
with col2:
    user_input = st.text_input("", placeholder="Frag mich etwas...", label_visibility="collapsed")
with col3:
    st.button("...")  # Uploadsymbol (optisch)

# --- Verarbeiten ---
if user_input:
    optimized = optimize_prompt(user_input)
    gpt_response = ask_gpt(optimized)
    st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
    st.rerun()

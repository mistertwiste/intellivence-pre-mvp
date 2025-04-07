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
        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            margin-top: 2rem;
        }
        .sidebar-icons button {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Init OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Optimizer (Dummy)
def optimize_prompt(user_input):
    return f"Optimierter Prompt: {user_input.strip().capitalize()}?"

# GPT

def ask_gpt(optimized_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": optimized_prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Fehler bei GPT]: {e}"

# Sidebar left menu
with st.sidebar:
    st.markdown("## ≡ Menü")
    st.markdown("<div class='sidebar-icons'>", unsafe_allow_html=True)
    st.button("👤")  # Profil
    st.button("★")  # Gespeichert
    st.button("📅")  # Kalender
    st.button("✉")  # Nachrichten
    st.button("!")  # Feedback
    st.button("?")  # Hilfe
    st.markdown("</div>", unsafe_allow_html=True)

# Title & instructions
st.markdown("# Hallo, wie kann ich dir helfen?")
st.markdown("Dies ist ein funktionaler MVP mit optischen Platzhaltern.")

# Chatverlauf
for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-text'><strong>CORE:</strong> {entry['gpt']}</div>", unsafe_allow_html=True)

# Eingabebereich unten zentriert
with st.container():
    st.markdown("""
    <div class="input-container">
        <button disabled>🎤</button>
        <input id="user_input" name="user_input" placeholder="Schreib etwas..." style="width: 400px; height: 35px; border-radius: 6px; padding: 5px;" />
        <button disabled>⤴</button>
    </div>
    <script>
    const inputBox = window.parent.document.querySelector('#user_input');
    inputBox.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const input = inputBox.value;
            fetch('/_stcore/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: input })
            });
        }
    });
    </script>
    """, unsafe_allow_html=True)

# Backup-Textfeld zum Verarbeiten in Streamlit direkt
user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed")

if user_input:
    optimized = optimize_prompt(user_input)
    gpt_response = ask_gpt(optimized)
    st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
    st.rerun()

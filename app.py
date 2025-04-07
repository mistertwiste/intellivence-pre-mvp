import streamlit as st
from utils import optimize_prompt, ask_gpt

st.set_page_config(page_title="Intellivence Pre-MVP", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Lexend', sans-serif;
    }
    .bottom-bar {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        display: flex;
        gap: 0.5rem;
    }
    .chat-box {
        min-height: 400px;
        margin-bottom: 4rem;
    }
    .menu-button {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 10;
    }
    </style>
""", unsafe_allow_html=True)

# Menü oben
with st.expander("≡ Menü", expanded=False):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.button("👤 Profil")
    with col2:
        st.button("⭐ Gespeichert")
    with col3:
        st.button("📅 Kalender")
    with col4:
        st.button("💬 Nachrichten")
    with col5:
        st.button("❗ Feedback")
    with col6:
        st.button("❓ Hilfe")

# Titel
st.markdown("## Hallo, wie kann ich dir helfen?")
st.markdown("Dies ist ein funktionaler MVP mit optischen Platzhaltern.")

# Chatverlauf
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}")
    st.markdown(f"**CORE:** {entry['gpt']}")

# Texteingabe unten mittig
with st.container():
    st.markdown("""<div class='bottom-bar'>""", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Schreib etwas...", label_visibility="collapsed", key="input")
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.button("...", help="Uploadsymbol (optisch)")
    with col2:
        if st.button("⏎" if not st.session_state.get("is_typing") else "⏹"):
            if not st.session_state.get("is_typing"):
                if user_input.strip():
                    st.session_state.is_typing = True
                    optimized = optimize_prompt(user_input)
                    gpt_response = ask_gpt(optimized)
                    st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
                    st.session_state.input = ""
                    st.session_state.is_typing = False
            else:
                st.session_state.is_typing = False  # Sofort stoppen
    st.markdown("""</div>""", unsafe_allow_html=True)

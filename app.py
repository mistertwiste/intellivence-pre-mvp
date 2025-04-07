import streamlit as st
import openai

st.set_page_config(page_title="Intellivence Pre-MVP", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def optimize_prompt(user_input):
    return f"Optimierter Prompt: {user_input.strip().capitalize()}?"

def ask_gpt(optimized_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": optimized_prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Fehler bei GPT]: {e}"

with st.sidebar:
    st.markdown("### 🔹 Navigation")
    st.button("Profil")
    st.button("Neuer Chat")
    st.button("Kalender (optisch)")
    st.button("Gespeichert (optisch)")
    st.button("Nachrichten-Zentrum (optisch)")
    st.button("Feedback (optisch)")
    st.markdown("---")
    st.button("🚩 Hilfe")

st.title("🤖 Intellivence Pre-MVP")
st.markdown("Dies ist eine funktionale Demo mit optischen Platzhaltern für UI-Komponenten.")

for entry in st.session_state.chat_history:
    st.markdown(f"**Du:** {entry['user']}")
    st.markdown(f"**CORE:** {entry['gpt']}")

st.markdown("---")
st.markdown("**Deine Eingabe:**")

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col1:
    st.button("🎤")
with col2:
    user_input = st.text_input("", placeholder="Stelle deine Frage...", label_visibility="collapsed")
with col3:
    st.button("...")

if user_input:
    optimized = optimize_prompt(user_input)
    gpt_response = ask_gpt(optimized)
    st.session_state.chat_history.append({"user": user_input, "gpt": gpt_response})
    st.experimental_rerun()

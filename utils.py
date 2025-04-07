import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Sicher in deiner Umgebung setzen

def optimize_prompt(prompt: str) -> str:
    return prompt.strip()

def ask_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

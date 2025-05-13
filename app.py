import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Groq API setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Email Draft Generator", layout="centered")
st.title(" LLM-Powered Email Draft Generator (LLaMA 3)")

# Input fields
subject = st.text_input("📌 Email Subject", placeholder="E.g., Apology for Delivery Delay")
greeting = st.text_input("🙋‍♂️ Greeting", placeholder="E.g., Dear Mr. White")
context = st.text_area("📝 Describe the purpose of the email", placeholder="E.g., Apologizing to a customer for a late delivery...")
tone = st.selectbox("🎭 Choose the tone", ["Formal", "Friendly", "Apologetic", "Assertive", "Enthusiastic"])
closing = st.text_input("🤝 Closing Statement", placeholder="E.g., Best regards")
sender_name = st.text_input("✍️ Your Name", placeholder="E.g., Jane Doe")

# Generate button
if st.button("Generate Email"):
    if all([subject, greeting, context, tone, closing, sender_name]):
        with st.spinner("Generating email using LLaMA 3..."):
            prompt = f"""
Write a professional email using the following information:
Subject: {subject}
Greeting: {greeting}
Context: {context}
Tone: {tone}
Closing: {closing}
Sender Name: {sender_name}

Ensure the email is clear, well-formatted, and follows professional best practices.
"""

            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }

            try:
                res = requests.post(GROQ_URL, headers=HEADERS, json=payload)
                res.raise_for_status()
                email = res.json()['choices'][0]['message']['content']
                st.success("✅ Email generated!")
                st.text_area("✉️ Drafted Email", value=email, height=300)
                st.download_button("⬇️ Download Email", email, file_name="email.txt")

                # Feedback section after generation
                st.markdown("---")
                st.subheader("💬 Feedback")
                feedback = st.text_area("Let us know how we can improve this tool:")
                if st.button("Submit Feedback"):
                    st.success("✅ Thank you for your feedback!")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error while communicating with Groq API: {e}")
    else:
        st.warning("⚠️ Please fill out all fields before generating the email.")

import streamlit as st
import requests

# --- CONFIGURATION ---
# Replace with your Hugging Face Token (Keep this private!)
HF_TOKEN = "your_hugging_face_token_here"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="MediVault AI", page_icon="💊", layout="centered")

# --- UI DESIGN ---
st.title("💊 MediVault AI: Disease & Medication Assistant")
st.markdown("""
This assistant provides detailed information on **100+ diseases**, including descriptions, 
treatments, and commonly used medications. 
""")

st.error("**Important Disclaimer:** This is an AI tool. Medication should only be taken under the supervision of a licensed doctor. Never self-medicate for serious conditions.")

# --- EMERGENCY DETECTION ---
EMERGENCY_WORDS = ["heart attack", "stroke", "bleeding heavily", "unconscious", "cannot breathe"]

def query_ai(prompt):
    """Sends user query to the medical-tuned AI model"""
    # System instruction to ensure it acts as a medical assistant
    payload = {
        "inputs": f"<|system|>\nYou are a professional medical assistant. Provide clear descriptions, common treatments, and specific medications for diseases. Always include a disclaimer that a doctor must be consulted.\n<|user|>\n{prompt}\n<|assistant|>\n",
        "parameters": {"max_new_tokens": 500, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text'].split("<|assistant|>\n")[-1]

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about a disease (e.g., 'What is the treatment and medication for Typhoid?')"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check for emergency
    if any(word in prompt.lower() for word in EMERGENCY_WORDS):
        bot_response = "🚨 **EMERGENCY:** This sounds like a life-threatening situation. Please call your local emergency number (e.g., 911) immediately."
    else:
        with st.spinner("Analyzing medical database..."):
            try:
                bot_response = query_ai(prompt)
            except Exception as e:
                bot_response = "I'm having trouble connecting to the database. Please try again in a moment."

    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

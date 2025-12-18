import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(
    page_title="AidLynx: Medical & First-Aid Assistant",
    page_icon="🚑",
    layout="wide"
)

# 2. Knowledge Base (Descriptions & First Aid)
KNOWLEDGE_BASE = {
    "choking": {
        "desc": "Airway obstruction by a foreign object.",
        "aid": "1. Perform Heimlich maneuver (abdominal thrusts). 2. Call emergency services. 3. If unconscious, start CPR."
    },
    "heart attack": {
        "desc": "Blood flow to the heart is blocked.",
        "aid": "1. Call emergency services immediately. 2. Have person sit/lie down. 3. Give aspirin if not allergic."
    },
    "heat stroke": {
        "desc": "Body overheating due to prolonged exposure to high heat.",
        "aid": "1. Move to a cool place. 2. Cool with water/ice packs. 3. Do NOT give fluids if they are confused."
    },
    "diabetes / low blood sugar": {
        "desc": "Hypoglycemia (too much insulin or not enough food).",
        "aid": "1. If conscious, give 15g of fast-acting sugar (soda, juice, candy). 2. Wait 15 mins, repeat if needed."
    },
    "seizure": {
        "desc": "Sudden electrical disturbance in the brain.",
        "aid": "1. Clear the area of sharp objects. 2. Place something soft under the head. 3. Do NOT restrain or put objects in mouth."
    }
}

# 3. Emergency Signals
RED_FLAGS = ["unconscious", "chest pain", "bleeding heavily", "not breathing", "stroke", "poisoning"]

# 4. Logic Functions
def check_emergency(text):
    text = text.lower()
    return any(flag in text for flag in RED_FLAGS)

def get_advice(user_input):
    user_input = user_input.lower()
    
    # Priority 1: Emergency Red Flags
    if check_emergency(user_input):
        return "🚨 **EMERGENCY DETECTED** 🚨\nStop what you are doing and **Call 911 / Local Emergency Services** immediately. Do not wait for this app to finish."

    # Priority 2: Knowledge Match
    for condition, data in KNOWLEDGE_BASE.items():
        if condition in user_input:
            return f"### {condition.title()}\n**Description:** {data['desc']}\n\n**First Aid Steps:**\n{data['aid']}"

    return "I'm sorry, I don't have specific first aid for that. Please seek a medical professional or try keywords like 'Choking' or 'Heat Stroke'."

# 5. UI Layout
st.title("🚑 AidLynx Assistant")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("How can I help you today?")
    user_query = st.chat_input("Describe the symptoms or situation...")
    
    if user_query:
        response = get_advice(user_query)
        st.info(f"**You:** {user_query}")
        st.success(f"**AidLynx:** \n{response}")

with col2:
    st.warning("**Disclaimer:** This tool provides general guidance. It is NOT a substitute for professional medical advice, diagnosis, or treatment.")
    st.subheader("Common Topics")
    for key in KNOWLEDGE_BASE.keys():
        if st.button(key.title()):
            st.write(f"**Description:** {KNOWLEDGE_BASE[key]['desc']}")
            st.write(f"**Aid:** {KNOWLEDGE_BASE[key]['aid']}")

import re
import streamlit as st

st.set_page_config(page_title="AidLynx", layout="centered")

WELCOME = (
    "Welcome to AidLynx.\n\n"
    "This site provides general health information and basic first-aid guidance in English.\n"
    "It does not diagnose diseases and is not a substitute for a doctor."
)

DISCLAIMER = (
    "Medical disclaimer: This is general information, not medical diagnosis or treatment. "
    "If symptoms are severe, worsening, or you suspect an emergency, contact local emergency services immediately."
)

# Emergency signals (simple keyword screening)
RED_FLAGS = [
    "not breathing", "stopped breathing", "unconscious", "unresponsive",
    "severe bleeding", "bleeding won't stop", "chest pain", "pressure in chest",
    "stroke", "face droop", "slurred speech", "one sided weakness",
    "seizure", "convulsion", "blue lips", "severe burn", "severe allergic",
    "anaphylaxis", "suicidal", "self harm"
]

# A broad condition library (you can keep adding names here)
CONDITIONS = {
    # Respiratory / ENT
    "common cold": "Usually mild viral illness. Focus: rest, fluids, monitor breathing.",
    "influenza (flu)": "Often fever/body aches. Seek care if high-risk or worsening.",
    "sinusitis": "Facial pressure + congestion can occur. Seek care if severe/persistent.",
    "sore throat": "Often viral; watch for trouble swallowing/breathing.",
    "tonsillitis": "Throat pain; seek care if high fever, dehydration, or breathing issues.",
    "bronchitis": "Cough; seek care if shortness of breath or high fever.",
    "pneumonia": "Can be serious. Seek medical evaluation if fever + breathing difficulty.",
    "asthma flare": "Wheezing/shortness of breath. Urgent care if severe breathing trouble.",
    "allergic rhinitis": "Sneezing/runny nose; avoid triggers when possible.",

    # Gastro / hydration
    "gastroenteritis": "Vomiting/diarrhea; focus on hydration, watch dehydration signs.",
    "food poisoning": "GI symptoms after food; hydrate, seek care if blood/high fever.",
    "diarrhea": "Hydration is key; urgent care if blood, severe pain, dehydration.",
    "constipation": "Often diet/fluids/activity-related; seek care if severe pain.",
    "acid reflux (gerd)": "Burning after meals; seek care for chest pain or red flags.",
    "peptic ulcer": "Stomach pain; urgent care if black stools or vomiting blood.",

    # Skin
    "eczema": "Itchy, inflamed skin; avoid irritants; seek care if infected.",
    "contact dermatitis": "Rash after exposure; remove trigger; seek care if severe swelling.",
    "fungal skin infection": "Itchy scaling; keep area clean/dry; clinician if spreading.",
    "acne": "Common; seek dermatology if painful/scarring.",
    "cellulitis": "Spreading redness/warmth can be serious; medical evaluation needed.",
    "hives (urticaria)": "Itchy welts; urgent care if swelling of lips/tongue/breathing trouble.",

    # Fever-region specific examples (still general)
    "dengue": "Fever with body aches; urgent care for bleeding, severe abdominal pain, fainting.",
    "malaria": "Fever with chills; needs testing; seek medical evaluation promptly.",
    "typhoid": "Prolonged fever; needs clinician evaluation.",
    "tuberculosis (tb)": "Chronic cough/weight loss/night sweats; needs clinician testing.",

    # Urinary / reproductive (general, non-diagnostic)
    "urinary tract infection (uti)": "Burning/frequency; urgent care if fever/flank pain/pregnancy.",
    "kidney stone": "Severe side pain; urgent care if fever/vomiting/uncontrolled pain.",

    # Chronic / metabolic (education only)
    "diabetes": "Long-term condition; urgent care for confusion, severe weakness, fainting.",
    "hypertension": "Often no symptoms; urgent care for severe headache/chest pain/neurologic signs.",

    # Neuro
    "tension headache": "Often band-like pressure; urgent care if sudden worst headache.",
    "migraine": "Throbbing headache + sensitivity; urgent care for weakness/confusion.",
    "vertigo": "Spinning sensation; urgent care if stroke-like signs.",

    # Injuries / first aid topics (not diseases, but requested first-aid)
    "cut / wound": "Control bleeding, clean, cover; urgent care if deep or won’t stop bleeding.",
    "burn": "Cool with running water, protect; urgent care for large/deep/chemical burns.",
    "sprain": "Rest/ice/compression/elevation; seek care if cannot bear weight.",
    "fracture": "Immobilize; urgent care if deformity/severe pain/poor circulation.",
    "nosebleed": "Lean forward, pinch soft nose; urgent care if heavy >20 min."
}

def normalize(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

def looks_like_emergency(text: str) -> bool:
    t = normalize(text)
    return any(flag in t for flag in RED_FLAGS)

def best_condition_match(text: str):
    t = normalize(text)
    # simple matching: exact key contained in user text
    for k in CONDITIONS.keys():
        if k in t:
            return k
    return None

def safe_reply(user_text: str) -> str:
    if looks_like_emergency(user_text):
        return (
            f"{DISCLAIMER}\n\n"
            "This may be an emergency.\n"
            "- Contact your local emergency number now.\n"
            "- If the person is unconscious or not breathing, get emergency help immediately.\n"
            "- If there is severe bleeding, apply firm pressure with a clean cloth while help is coming."
        )

    match = best_condition_match(user_text)
    if match:
        return (
            f"{DISCLAIMER}\n\n"
            f"Topic: {match.title()}\n"
            f"- General info: {CONDITIONS[match]}\n"
            "- Seek urgent care now if you have trouble breathing, chest pain, fainting, severe bleeding, "
            "severe dehydration, confusion, or symptoms that rapidly worsen.\n"
            "- Helpful details to share: age, duration, fever (temperature), current medicines, major illnesses."
        )

    return (
        f"{DISCLAIMER}\n\n"
        "Choose a menu option (left) or describe symptoms.\n"
        "For best guidance, include: age, main symptoms, when it started, fever temperature (if any), "
        "known conditions, and current medicines."
    )

# UI
st.title("AidLynx")
st.write(WELCOME)

with st.expander("Medical disclaimer"):
    st.write(DISCLAIMER)

# Sidebar menu buttons
st.sidebar.header("Menu")
st.sidebar.caption("Tap a button to start quickly.")

MENU = [
    ("Fever", "I have fever. What should I do?"),
    ("Cough / cold", "I have cough and cold symptoms."),
    ("Sore throat", "I have sore throat."),
    ("Diarrhea", "I have diarrhea."),
    ("Vomiting", "I have vomiting."),
    ("Headache", "I have headache."),
    ("Allergy / hives", "I have allergy or hives."),
    ("Burn", "I got a burn. First aid steps?"),
    ("Cut / bleeding", "I have a cut and bleeding. First aid steps?"),
    ("Sprain", "I twisted my ankle. First aid steps?"),
]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": safe_reply("hello")}]

def push_user_message(text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    st.session_state.messages.append({"role": "assistant", "content": safe_reply(text)})

for label, prompt in MENU:
    if st.sidebar.button(label, use_container_width=True):
        push_user_message(prompt)

st.sidebar.divider()
st.sidebar.subheader("Condition library")
query = st.sidebar.text_input("Search (e.g., asthma, dengue, uti)")
q = normalize(query)
matches = [k for k in CONDITIONS.keys() if q and q in k]
if matches:
    pick = st.sidebar.selectbox("Select", matches[:30])
    if st.sidebar.button("Show info", use_container_width=True):
        push_user_message(f"Tell me about {pick}.")

# Chat transcript
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

text = st.chat_input("Type your question in English...")
if text:
    push_user_message(text)
    st.rerun()

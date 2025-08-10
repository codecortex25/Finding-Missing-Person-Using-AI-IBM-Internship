import streamlit as st
from datetime import datetime
from pages.helper.data_models import RegisteredCases
from pages.helper import db_queries
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ========== Load environment variables ==========
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠ GEMINI_API_KEY is missing in .env file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# ========== Helper Function to Call Gemini ==========
def generate_ai_alert(prompt: str) -> str:
    """
    Calls Google Gemini API to generate a missing person alert text.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[AI Generation Failed] {str(e)}"

# ========== Streamlit UI ==========
st.title("Register New Missing Person Case")

# User input form
with st.form("register_case_form"):
    submitted_by = st.text_input("Submitted By")
    name = st.text_input("Missing Person's Name")
    father_name = st.text_input("Father's Name")
    age = st.text_input("Age")
    complainant_name = st.text_input("Complainant Name")
    complainant_mobile = st.text_input("Complainant Mobile")
    adhaar_card = st.text_input("Aadhaar Card Number")
    last_seen = st.text_input("Last Seen Location")
    address = st.text_area("Address")
    birth_marks = st.text_area("Birth Marks / Identification Marks")
    face_mesh = st.text_area("Face Mesh JSON")

    submit_btn = st.form_submit_button("Register Case")

if submit_btn:
    # Save case in DB
    case = RegisteredCases(
        submitted_by=submitted_by,
        name=name,
        father_name=father_name,
        age=age,
        complainant_name=complainant_name,
        complainant_mobile=complainant_mobile,
        adhaar_card=adhaar_card,
        last_seen=last_seen,
        address=address,
        face_mesh=face_mesh,
        submitted_on=datetime.utcnow(),
        status="NF",  # Not Found
        birth_marks=birth_marks,
        matched_with=None
    )
    case_id = db_queries.register_new_case(case)

    # Generate AI alert using Gemini
    prompt = f"""
    Create a concise but impactful public missing person alert based on this case:
    Name: {name}
    Age: {age}
    Last Seen: {last_seen}
    Birth Marks: {birth_marks}
    Please write in a way suitable for WhatsApp and social media posting.
    """

    alert_text = generate_ai_alert(prompt)

    # Save alert to DB
    try:
        db_queries.save_alert(case.id, alert_text)
    except Exception as e:
        st.error(f"Failed to save AI alert to DB: {e}")

    # Show results
    st.success("✅ Case registered successfully!")
    if "AI Generation Failed" in alert_text:
        st.warning(alert_text)
    else:
        st.subheader("AI-generated Alert")
        st.write(alert_text)

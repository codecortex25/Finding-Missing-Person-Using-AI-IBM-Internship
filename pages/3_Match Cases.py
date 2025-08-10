import streamlit as st
from pages.helper import db_queries
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠ GEMINI_API_KEY not found in .env file")
else:
    genai.configure(api_key=GEMINI_API_KEY)

st.title("Match Registered & Public Cases")

# Fetch NF registered cases
registered_cases = db_queries.fetch_registered_cases(submitted_by="admin", status="Not Found")
public_cases = db_queries.fetch_public_cases(train_data=False, status="NF")

if not registered_cases or not public_cases:
    st.warning("No cases available for matching.")
else:
    reg_case_id = st.selectbox("Select Registered Case", [r[0] for r in registered_cases])
    pub_case_id = st.selectbox("Select Public Case", [p[0] for p in public_cases])

    if st.button("Mark as Match"):
        db_queries.update_found_status(reg_case_id, pub_case_id)

        try:
            # Fetch case details
            reg_details = db_queries.get_registered_case_detail(reg_case_id)
            pub_details = db_queries.get_public_case_detail(pub_case_id)

            # 1️⃣ Match explanation
            prompt_exp = f"""
            You are an investigator. Based on the following two reports,
            explain concisely why these cases are a probable match.

            Registered Case: {reg_details}
            Public Submission: {pub_details}
            """
            model = genai.GenerativeModel("gemini-1.5-flash")
            match_response = model.generate_content(prompt_exp)
            match_explanation = match_response.text.strip()
            db_queries.save_match_explanation(reg_case_id, match_explanation)

            # 2️⃣ Witness summary
            prompt_summary = f"""
            Summarize the witness/public submission details in a clear, concise way for law enforcement.
            Public Submission: {pub_details}
            """
            witness_response = model.generate_content(prompt_summary)
            witness_summary = witness_response.text.strip()
            db_queries.save_witness_summary(reg_case_id, witness_summary)

            # ✅ Success display
            st.success("Cases matched and AI explanations saved.")
            st.subheader("AI Match Explanation")
            st.write(match_explanation)
            st.subheader("AI Witness Summary")
            st.write(witness_summary)

        except Exception as e:
            st.warning(f"Match saved, but AI generation failed: {e}")

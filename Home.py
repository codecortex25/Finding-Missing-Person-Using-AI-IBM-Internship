import streamlit as st
import streamlit_authenticator as stauth
import yaml
import base64
from yaml import SafeLoader

from pages.helper import db_queries
st.set_page_config("Admin/ Main ", initial_sidebar_state="auto")
# print("Dhruvil Nakrani")

# ✅ Background Image Setup
def add_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: top left;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# 🔧 Initialize session state
if "login_status" not in st.session_state:
    st.session_state["login_status"] = False

# ✅ Load login credentials config
try:
    with open("login_config.yml") as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Configuration file 'login_config.yml' not found.")
    st.stop()

# ✅ Initialize authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# ✅ Perform login
authenticator.login(location="main")

# ✅ After login
if st.session_state.get("authentication_status"):

    # Show logout button
    authenticator.logout("Logout", "sidebar")

    # Mark login as successful
    st.session_state["login_status"] = True

    # Extract user info from config
    st.session_state["login_status"] = True
    user_info = config["credentials"]["usernames"][st.session_state["username"]]
    st.session_state["user"] = user_info["name"]
    
    # ✅ Display user profile info
    st.markdown(
        f"""
        <h1 style='color:#888;'>{user_info['name']}</h1>
        <h4 style='color:#444;'>{user_info['area']}, {user_info['city']}</h4>
        <h5 style='color:#888;'>Role: {user_info['role']}</h5>
        <hr>
        """, unsafe_allow_html=True
    )

    # ✅ Show dashboard metrics
    found_cases = db_queries.get_registered_cases_count(user_info["name"], "F")
    not_found_cases = db_queries.get_registered_cases_count(user_info["name"], "NF")

    col1, col2 = st.columns(2)
    col1.metric("🟢 Found Cases", value=len(found_cases))
    col2.metric("🟠 Not Found Cases", value=len(not_found_cases))

# ❌ Incorrect Login
elif st.session_state.get("authentication_status") is False:
    st.error("❌ Username or password is incorrect.")

# ⏳ Before Login
elif st.session_state.get("authentication_status") is None:
    st.warning("🔐 Please enter your username and password.")
    st.session_state["login_status"] = False

st.sidebar.header("Admin GenAI Tools")
case_to_regen = st.sidebar.text_input("Case ID to (re)generate alert/explanation", value="")
if st.sidebar.button("Regenerate GenAI outputs") and case_to_regen:
    try:
        from pages.helper.genai_agent import generate_alert, explain_matches
        # Fetch case details
        rec = db_queries.get_registered_case_detail(case_to_regen)[0]
        case_dict = {"id": case_to_regen, "name": rec[0], "last_seen": rec[4] if len(rec)>4 else ""}
        alert = generate_alert(case_dict)
        st.sidebar.success("Alert regenerated (preview below).")
        st.sidebar.write(alert.get("short", str(alert)))
    except Exception as e:
        st.sidebar.error(f"Failed: {str(e)}")

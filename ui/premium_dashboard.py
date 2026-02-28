import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Incident AI Command Center",
    layout="wide"
)

# ==============================
# PREMIUM AI THEME
# ==============================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#020617,#020617,#0f172a);
    color: white;
}

section[data-testid="stSidebar"] {
    background-color:#020617;
}

h1,h2,h3 {
    color:#00f5ff;
    text-shadow:0px 0px 12px #00f5ff;
}

div[data-testid="metric-container"] {
    background:rgba(255,255,255,0.05);
    border-radius:15px;
    padding:15px;
    box-shadow:0 0 20px rgba(0,255,255,0.2);
}

.stButton button {
    background:linear-gradient(90deg,#00f5ff,#6366f1);
    color:white;
    border:none;
    border-radius:10px;
    font-weight:bold;
}

[data-testid="stDataFrame"] {
    background:rgba(255,255,255,0.04);
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# AUTO REFRESH (10s)
# ==============================
st_autorefresh(interval=10000, key="refresh")

API = "http://127.0.0.1:8000"

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("🤖 Incident AI")

token = st.sidebar.text_input(
    "Access Token",
    type="password"
)

headers = {}
if token:
    headers["Authorization"] = "Bearer " + token

page = st.sidebar.radio(
    "Navigation",
    ["AI Dashboard", "Create Incident", "Incidents"]
)

st.title("🚀 Incident AI Command Center")
st.success("🟢 AI Monitoring Active")

# =====================================================
# DASHBOARD
# =====================================================
if page == "AI Dashboard":

    st.subheader("📊 AI Incident Overview")

    if not token:
        st.warning("Enter access token")

    else:
        response = requests.get(
            API + "/incidents",
            headers=headers
        )

        if response.status_code != 200:
            st.error("Failed to fetch incidents")

        else:
            data = response.json()

            if isinstance(data, list) and len(data) > 0:

                df = pd.DataFrame(data)

                c1, c2, c3 = st.columns(3)

                c1.metric("Total Incidents", len(df))

                critical = len(
                    df[df["severity"].str.contains(
                        "CRITICAL", case=False, na=False)]
                )

                high = len(
                    df[df["severity"].str.contains(
                        "HIGH", case=False, na=False)]
                )

                c2.metric("Critical", critical)
                c3.metric("High", high)

                fig = px.pie(
                    df,
                    names="severity",
                    title="Incident Severity"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

            else:
                st.info("No incidents found")

# =====================================================
# CREATE INCIDENT
# =====================================================
elif page == "Create Incident":

    st.subheader("🧠 Create AI Incident")

    msg = st.text_area("Describe Incident")

    if st.button("Run AI Analysis"):

        if not token:
            st.warning("Enter access token")

        elif not msg:
            st.warning("Enter incident message")

        else:
            r = requests.post(
                API + "/incident",
                json={"message": msg},
                headers=headers
            )

            if r.status_code == 201:
                st.success("✅ Incident Created")
                st.json(r.json())
            else:
                st.error("Incident creation failed")

# =====================================================
# INCIDENT LIST
# =====================================================
elif page == "Incidents":

    st.subheader("📂 Incident List")

    if not token:
        st.warning("Enter access token")

    else:
        response = requests.get(
            API + "/incidents",
            headers=headers
        )

        if response.status_code != 200:
            st.error("Failed to load incidents")

        else:
            incidents = response.json()

            if len(incidents) == 0:
                st.info("No incidents available")

            for i in incidents:

                severity = i["severity"].upper()

                if "CRITICAL" in severity:
                    color = "#ff4b4b"
                elif "HIGH" in severity:
                    color = "#ffa500"
                else:
                    color = "#00ffcc"

                st.markdown(
                    f"<h4 style='color:{color}'>🚨 Incident {i['id']}</h4>",
                    unsafe_allow_html=True
                )

                st.write("**Message:**", i["alert_message"])
                st.write("**Status:**", i["status"])
                st.write("**Severity:**", i["severity"])

                st.divider()
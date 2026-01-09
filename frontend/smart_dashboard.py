import streamlit as st
import requests
import datetime
import numpy as np
import pandas as pd

st.set_page_config(page_title="🏙️ Smart City Assistant", layout="wide")
st.sidebar.title("🏙️ Smart City Assistant")

BACKEND_URL = "http://localhost:8000"

selected_city = st.sidebar.text_input("🏙️ Enter City Name (manual):")

page = st.sidebar.radio("📋 Select a Page", [
    "Dashboard Summary", "Citizen Feedback", "Eco Tips", "KPI Forecasting",
    "Anomaly Detection", "Sustainability Report", "Policy Summarizer", "Chat Assistant"
])

st.title(f"{page} - {selected_city if selected_city else 'No City Selected'}")

def get_sample_kpi_data():
    dates = pd.date_range(datetime.date.today(), periods=7)
    return pd.DataFrame({
        "Date": dates,
        "Energy Usage (MWh)": np.random.randint(500, 1000, 7),
        "Water Consumption (ML)": np.random.randint(200, 400, 7),
        "Waste Collected (Tons)": np.random.randint(50, 100, 7)
    })

if page == "Dashboard Summary":
    st.subheader(f"Smart Dashboard Overview - City: {selected_city}")
    if selected_city:
        try:
            resp = requests.get(f"{BACKEND_URL}/kpi/forecast", params={"city": selected_city})
            data = resp.json()
            if "error" in data:
                st.warning(data["error"])
            else:
                water_usage = data.get("Estimated Water Usage (Liters)", "N/A")
                energy_usage = data.get("Estimated Energy Consumption (kWh)", "N/A")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💧 Water Usage", f"{water_usage} Liters")
                with col2:
                    st.metric("⚡ Energy Consumption", f"{energy_usage} kWh")
        except Exception as e:
            st.error(f"Error fetching KPI data: {e}")
    else:
        st.info("Please enter a city name.")

elif page == "Citizen Feedback":
    st.subheader("Submit Your Feedback or Report an Issue")
    name = st.text_input("Your Name")
    issue_type = st.selectbox("Type of Issue", ["Garbage", "Water Supply", "Electricity", "Roads", "Others"])
    description = st.text_area("Describe the issue or suggestion")
    if st.button("Submit Feedback"):
        if name and description:
            payload = {"name": name, "message": f"Issue: {issue_type} - {description}"}
            try:
                resp = requests.post(f"{BACKEND_URL}/feedback/submit", json=payload)
                if resp.status_code == 200:
                    st.success("✅ Feedback submitted successfully!")
                else:
                    st.error(f"❌ Backend error: {resp.status_code}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
        else:
            st.warning("⚠️ Please fill all fields.")

elif page == "Eco Tips":
    st.subheader("🌱 Eco Tip Generator (AI Powered)")
    topic = st.text_input("Enter a topic for your eco tip")
    if st.button("Get Eco Tip"):
        if topic:
            with st.spinner("Getting tip..."):
                try:
                    resp = requests.post(f"{BACKEND_URL}/eco/tips", json={"topic": topic})
                    result = resp.json()
                    if "tip" in result:
                        st.success(result["tip"])
                    else:
                        st.error(result.get("error", "Failed to get tip."))
                except Exception as e:
                    st.error(e)
        else:
            st.warning("Please enter a topic.")

elif page == "KPI Forecasting":
    st.subheader("📈 KPI Forecast")
    st.line_chart(get_sample_kpi_data().set_index("Date"))

elif page == "Anomaly Detection":
    st.subheader(f"⚠️ Detected Anomalies - {selected_city}")
    if selected_city:
        try:
            resp = requests.get(f"{BACKEND_URL}/anomaly/check", params={"city": selected_city})
            result = resp.json()
            if "anomalies" in result:
                df = pd.DataFrame(result["anomalies"])
                st.table(df[["Date", "Type", "Severity"]])
            else:
                st.warning("No anomalies found.")
        except Exception as e:
            st.error(f"Error fetching anomalies: {e}")
    else:
        st.info("Please enter a city name.")

elif page == "Sustainability Report":
    st.subheader(f"📊 Sustainability Summary - {selected_city}")
    if selected_city:
        try:
            resp = requests.get(f"{BACKEND_URL}/sustainability/report", params={"city": selected_city})
            data = resp.json()
            if "error" in data:
                st.warning(data["error"])
            else:
                st.markdown(f"""
                - **City**: {data.get("City", selected_city)}
                - **Carbon Emissions**: {data.get("Carbon Emissions", "N/A")}
                - **Recycling Rate**: {data.get("Recycling Rate", "N/A")}
                - **Green Spaces**: {data.get("Green Spaces", "N/A")}
                - **EV Charging Stations**: {data.get("EV Charging Stations", "N/A")}
                """)
        except Exception as e:
            st.error(f"Error fetching sustainability report: {e}")
    else:
        st.info("Please enter a city name.")

elif page == "Policy Summarizer":
    st.subheader("📜 Policy Summarizer")
    txt = st.text_area("Paste a policy to summarize", height=200)
    if txt:
        if st.button("Summarize Policy"):
            with st.spinner("Summarizing..."):
                try:
                    resp = requests.post(f"{BACKEND_URL}/policy/summarize", json={"text": txt})
                    result = resp.json()
                    st.success(result.get("summary", resp.text))
                except Exception as e:
                    st.error(e)

elif page == "Chat Assistant":
    st.subheader("💬 Chat Assistant")
    chat = st.chat_input("Ask anything about Smart City")
    if chat:
        with st.spinner("Talking..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/chat/ask", json={"question": chat})
                result = resp.json()
                st.success(result.get("answer", resp.text))
            except Exception as e:
                st.error(e)

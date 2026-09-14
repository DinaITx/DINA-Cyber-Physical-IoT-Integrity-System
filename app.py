import random
import time
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DINACyber-Physical IoT Integrity System", layout="wide"
)

st.title("🛡️ DINA Cyber-Physical IoT Integrity System")
st.markdown(
    "Intelligent monitoring platform for detecting cyber manipulation and"
    " physical failures in IoT systems."
)
st.markdown("---")

if "history" not in st.session_state:
    st.session_state.history = []

if "log_records" not in st.session_state:
    st.session_state.log_records = []

st.sidebar.header("⚙️ Simulation Settings")
auto_refresh = st.sidebar.checkbox(
    "Enable Auto-Refresh (Live Stream)", value=False
)
refresh_rate = st.sidebar.slider(
    "Refresh Rate (seconds)", min_value=1, max_value=5, value=2
)

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Live Monitoring",
        "📈 Analytics & Reports",
        "🔒 Security Guidelines",
    ]
)

with tab1:
    current_time = pd.Timestamp.now().strftime("%H:%M:%S")
    status_options = [
        "Normal",
        "Suspicious",
        "Cyber Manipulation",
        "Physical Failure",
    ]
    status = random.choices(status_options, weights=[70, 10, 10, 10], k=1)[0]

    temp = round(random.uniform(20.0, 50.0), 2)
    network_rate = random.randint(20, 100)

    if status == "Cyber Manipulation":
        network_rate = random.randint(350, 700)
    elif status == "Physical Failure":
        temp = round(random.uniform(75.0, 95.0), 2)

    st.session_state.history.append({
        "Time": current_time,
        "Temperature": temp,
        "Network": network_rate,
    })
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

    if status != "Normal":
        details_text = (
            "Unjustified network traffic spike"
            if status == "Cyber Manipulation"
            else (
                "Sensor overheating detected"
                if status == "Physical Failure"
                else "Notable fluctuation detected"
            )
        )
        st.session_state.log_records.insert(
            0,
            {
                "Time": current_time,
                "Device": "ESP32-Node-01",
                "Status": status,
                "Details": details_text,
            },
        )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("System Status", status)
    col2.metric("Temperature (Physical)", f"{temp} °C")
    col3.metric("Packet Rate (Network)", f"{network_rate} pkts/s")
    col4.metric("Active Devices", "1 / 1")

    st.markdown("---")

    if status == "Normal":
        st.success(
            "🟢 System Stable: Physical behavior and network traffic are 100%"
            " consistent."
        )
    elif status == "Suspicious":
        st.warning(
            "🟡 Warning: Unusual pattern detected, monitoring behavior..."
        )
    elif status == "Cyber Manipulation":
        st.error(
            "🔴 Critical Alert! Cyber manipulation detected (Network traffic"
            " contradicts physical state)."
        )
    else:
        st.info(
            "🔵 Alert: Physical sensor failure detected (Network is normal while"
            " readings are invalid)."
        )

    st.subheader("📊 Live Behavior Streams")
    df_history = pd.DataFrame(st.session_state.history)
    if not df_history.empty:
        df_chart = df_history.set_index("Time")
        st.line_chart(df_chart)

    st.subheader("📋 Audit Logs")
    if st.session_state.log_records:
        df_logs = pd.DataFrame(st.session_state.log_records)
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info(
            "No security logs recorded yet, the system is running normally."
        )

    if st.button("🗑️ Clear Logs"):
        st.session_state.log_records = []
        st.rerun()

with tab2:
    st.subheader("📈 System Analytics & Historical Insights")
    st.markdown(
        "This section provides comprehensive analytics and statistics regarding"
        " detected system incidents."
    )

    if st.session_state.log_records:
        df_analytics = pd.DataFrame(st.session_state.log_records)

        total_alerts = len(df_analytics)
        cyber_count = len(
            df_analytics[df_analytics["Status"] == "Cyber Manipulation"]
        )
        physical_count = len(
            df_analytics[df_analytics["Status"] == "Physical Failure"]
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Recorded Alerts", total_alerts)
        c2.metric("Cyber Manipulation Incidents", cyber_count)
        c3.metric("Physical Failure Incidents", physical_count)

        st.markdown("---")
        st.subheader("📊 Distribution of Detected Statuses")
        status_counts = df_analytics["Status"].value_counts()
        st.bar_chart(status_counts)

        st.subheader("📄 Full Audit Trail Report")
        st.dataframe(df_analytics, use_container_width=True)
    else:
        st.info(
            "No sufficient data for analysis yet. Let the system run or wait"
            " for alerts to be recorded."
        )

with tab3:
    st.subheader("🔒 Security Guidelines & Best Practices for IoT")
    st.markdown(
        "Core recommendations and guidelines to enhance security for"
        " cyber-physical and IoT systems:"
    )

    st.markdown("""
    ### 1. Secure Communication Channels
    * Use encrypted and secure protocols such as **MQTT over TLS** or **HTTPS** for sensor data transmission to prevent eavesdropping or Man-in-the-Middle (MitM) attacks.
    
    ### 2. Cross-Layer Data Validation
    * Rely on algorithms that cross-check actual physical behavior (like temperature or pressure) against digital behavior (network traffic) to uncover stealthy attacks hiding behind spoofed readings.
    
    ### 3. Device Hardening and Factory Settings
    * Immediately change default credentials for ESP32 and Raspberry Pi hardware nodes.
    * Disable unused communication ports and debugging interfaces on field-deployed devices.
    
    ### 4. Continuous Monitoring and Audit Logging
    * Maintain centralized, tamper-evident audit logs to retrospectively analyze system anomalies and pinpoint exact root causes of failures.
    """)

if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
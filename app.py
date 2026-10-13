
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="UV Sentinel | MDP",
    page_icon="☀️",
    layout="wide"
)

# Premium dashboard styling
st.markdown("""
<style>
.stApp {
    background-color: #101820;
    color: #F4F1E8;
}
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
h1, h2, h3 {
    color: #F4F1E8 !important;
}
[data-testid="stMetric"] {
    background: #202D35;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #46545A;
}
div.stButton > button {
    border-radius: 7px;
    border: 1px solid #A5B6A0;
}
</style>
""", unsafe_allow_html=True)

def classify_uv(uv):
    if uv < 3:
        return "LOW", "Generally low risk", "#63C68B"
    elif uv < 6:
        return "MODERATE", "Use sun protection", "#F2CF60"
    elif uv < 8:
        return "HIGH", "Seek shade and protect your skin", "#F4A261"
    elif uv < 11:
        return "VERY HIGH", "Reduce direct sun exposure", "#F07167"
    return "EXTREME", "Avoid prolonged direct sun exposure", "#C77DFF"

st.title("☀️ UV SENTINEL")
st.caption("SMART UV INDEX WARNING SYSTEM  /  MDP PROTOTYPE")

st.warning(
    "SIMULATION MODE — All readings are manually selected "
    "or generated demo data, not real UV measurements."
)

st.divider()

# UV input
st.subheader("01 / Environmental Monitoring")
uv = st.slider(
    "Adjust simulated UV Index",
    min_value=0.0,
    max_value=15.0,
    value=3.0,
    step=0.5
)

risk, advice, color = classify_uv(uv)

# Main metrics
c1, c2, c3 = st.columns(3)
c1.metric("UV INDEX", f"{uv:.1f} / 15")
c2.metric("RISK CLASSIFICATION", risk)
c3.metric("WARNING STATUS", "ACTIVE" if uv >= 6 else "NORMAL")

# Visual risk meter
st.markdown("### UV Exposure Meter")
st.progress(int(uv / 15 * 100))

st.markdown(
    f"<div style='background:{color};color:#101820;"
    f"padding:18px;border-radius:9px;font-weight:700;'>"
    f"● {risk} RISK — {advice}</div>",
    unsafe_allow_html=True
)

st.caption(
    "UV categories: Low 0–2 | Moderate 3–5 | High 6–7 | "
    "Very High 8–10 | Extreme 11+"
)

st.divider()

# Hardware status panel
st.subheader("02 / Prototype Status")
h1, h2, h3 = st.columns(3)

h1.markdown("**Controller**")
h1.success("ESP32 — planned")

h2.markdown("**Warning LED**")
h2.write("🟢 ON" if uv >= 6 else "⚪ OFF")

h3.markdown("**Buzzer**")
h3.write("🔊 ON" if uv >= 8 else "🔇 OFF")

st.caption(
    "LED and buzzer states are simulated. No physical hardware "
    "is currently connected to this dashboard."
)

st.divider()

# Reading history
st.subheader("03 / Data Logging & Result Analysis")

if "history" not in st.session_state:
    st.session_state.history = []

b1, b2 = st.columns(2)

with b1:
    if st.button("＋ Record Current Reading", use_container_width=True):
        st.session_state.history.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "UV Index": uv,
            "Risk": risk
        })

with b2:
    if st.button("Generate Demo Day", use_container_width=True):
        demo_values = [1, 2, 4, 6, 8, 10, 12, 9, 7, 5, 3, 2]
        st.session_state.history = []
        for i, value in enumerate(demo_values):
            category, _, _ = classify_uv(value)
            st.session_state.history.append({
                "Time": f"{i:02d}:00",
                "UV Index": value,
                "Risk": category
            })

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    a, b, c = st.columns(3)
    a.metric("Recorded Samples", len(df))
    b.metric("Maximum UV", f"{df['UV Index'].max():.1f}")
    c.metric("Average UV", f"{df['UV Index'].mean():.1f}")

    st.markdown("#### UV Trend")
    st.line_chart(df.set_index("Time")["UV Index"])

    st.markdown("#### Reading Log")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        "Download CSV Report",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="smart_uv_demo_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Clear Reading History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info(
        "Record readings or click 'Generate Demo Day' "
        "to demonstrate result analysis."
    )

st.divider()
st.markdown("**SMART UV WARNING SYSTEM**  |  MDP ENGINEERING PROTOTYPE")
st.caption(
    "Future integration: calibrated UV sensor → ESP32 → live dashboard."
)

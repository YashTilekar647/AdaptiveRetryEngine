import streamlit as st, json
from collections import Counter

st.set_page_config(page_title="Adaptive Retry Engine", layout="wide")
st.title("🔁 Adaptive Retry Intelligence Engine")

logs = []
try:
    with open("logs/retry_log.json") as f:
        for line in f:
            logs.append(json.loads(line))
except:
    st.info("Run main.py first")
    st.stop()

events = Counter(l["event"] for l in logs)
failures = Counter(l.get("failure_type", "N/A") for l in logs)

c1, c2, c3 = st.columns(3)
c1.metric("Total Events", len(logs))
c2.metric("Retries", events.get("retry", 0))
c3.metric("Circuit Opens", events.get("circuit_open", 0))

st.bar_chart(failures)

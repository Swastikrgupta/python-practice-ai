import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Feedback Analyzer", page_icon="💬")
st.title("💬 Feedback Analyzer")

def call_api(method: str, path: str, **kwargs):
    try:
        response = requests.request(method, f"{API_URL}{path}", timeout=60, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        st.error("Could not reach the API. Is it running on port 8000?")
    except requests.RequestException as e:
        st.error(f"API error: {e}")
    return None

analyze_tab, history_tab = st.tabs(["Analyze", "History"])

with analyze_tab:
    st.write("Paste a customer review to get its sentiment, score, and main topic.")
    text = st.text_area("Review", height=150, placeholder="The food was delicious but the delivery took over an hour.")

    if st.button("Analyze", type="primary"):
        if not text.strip():
            st.warning("Please enter a review first.")
        else:
            with st.spinner("Analyzing..."):
                result = call_api("POST", "/analyze_review", json={"text": text})

            if result:
                label = result["label"].lower()
                if label == "positive":
                    st.success("Positive 😊")
                elif label == "negative":
                    st.error("Negative 😞")
                else:
                    st.info("Neutral 😐")

                col1, col2 = st.columns(2)
                col1.metric("Score", f"{result['score']} / 5")
                col2.metric("Service", result["service"])
                st.caption("Saved to history.")

with history_tab:
    st.button("Refresh")
    reviews = call_api("GET", "/reviews")

    if reviews == []:
        st.info("No reviews yet. Analyze one to see it here.")
    elif reviews:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total reviews", len(reviews))
        col2.metric("Average score", f"{sum(r['score'] for r in reviews) / len(reviews):.1f} / 5")
        col3.metric("Positive", f"{sum(r['label'].lower() == 'positive' for r in reviews) / len(reviews):.0%}")

        st.dataframe(
            reviews,
            column_order=["created_at", "text", "label", "score", "service"],
            column_config={
                "created_at": "Date",
                "text": st.column_config.TextColumn("Review", width="large"),
                "label": "Label",
                "score": "Score",
                "service": "Service",
            },
            hide_index=True,
            width="stretch",
        )

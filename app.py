"""Streamlit conversational interface for the FRED economic data assignment."""

import streamlit as st

from data_analysis import (
    answer_question,
    create_comparison_chart,
    load_economic_data,
)

st.set_page_config(page_title="Economic Data Recommendation Engine", page_icon="📈", layout="wide")
st.title("📈 Conversational AI for Economic Data Analysis")
st.caption("Ask questions about U.S. GDP and Core CPI using FRED data.")


@st.cache_data(ttl=3600)
def get_data():
    return load_economic_data()


try:
    data = get_data()
except Exception as error:
    st.error(f"Could not retrieve FRED data: {error}")
    st.info("Check your internet connection and try refreshing the page.")
    st.stop()


with st.sidebar:
    st.header("Example questions")
    examples = [
        "What is the latest reported U.S. GDP?",
        "How has GDP changed over the past 10 years?",
        "What is the current Core CPI inflation rate?",
        "What is the relationship between GDP growth and Core CPI inflation?",
    ]
    for example in examples:
        st.write(f"• {example}")
    st.divider()
    st.write("Data sources:")
    st.markdown("- [GDP series](https://fred.stlouisfed.org/series/GDP)")
    st.markdown("- [Core CPI series](https://fred.stlouisfed.org/series/CPILFESL)")
    st.info("Answers are calculated from live FRED data using Pandas.")


st.subheader("Ask the economic data assistant")
st.write("Enter one question below. Your answer will appear directly underneath.")

with st.form("question_form", clear_on_submit=False):
    question_input = st.text_input(
        "Question",
        placeholder="Example: What is the latest reported U.S. GDP?",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Ask the assistant", type="primary")

if "latest_exchange" not in st.session_state:
    st.session_state.latest_exchange = None

if submitted and question_input.strip():
    question = question_input.strip()
    response = answer_question(question, data)
    st.session_state.latest_exchange = {"question": question, "answer": response}

# Show only one exchange so the interface stays simple and easy to follow.
if st.session_state.latest_exchange:
    st.markdown("### Latest exchange")
    with st.container(border=True):
        st.markdown(f"**Question:** {st.session_state.latest_exchange['question']}")
        st.markdown(f"**Answer:** {st.session_state.latest_exchange['answer']}")
elif submitted:
    st.warning("Please enter a question before clicking Ask the assistant.")

st.divider()
with st.expander("Economic visualization", expanded=True):
    st.plotly_chart(create_comparison_chart(data["comparison"]), width="stretch")

csv_data = data["comparison"].to_csv(index=False).encode("utf-8")
st.download_button(
    "Download comparison data (CSV)",
    data=csv_data,
    file_name="gdp_core_cpi_comparison.csv",
    mime="text/csv",
)

with st.expander("View the latest raw observations", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write("GDP")
        st.dataframe(data["gdp"].tail(10), width="stretch", hide_index=True)
    with col2:
        st.write("Core CPI")
        st.dataframe(data["cpi"].tail(10), width="stretch", hide_index=True)


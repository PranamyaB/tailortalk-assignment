# streamlit_app.py
import streamlit as st
from langgraph_agent import run_agent
st.set_page_config(page_title="TailorTalk Calendar", layout="centered")
st.title("TailorTalk Calendar Assistant")
query = st.text_input("Ask me to schedule something", placeholder="e.g. Schedule a meeting tomorrow at 3 PM")
if st.button("Submit"):
    if query:
        with st.spinner("Agent is processing..."):
            response = run_agent(query)
        st.success("Response:")
        st.write(response or "No response returned.")
    else:
        st.warning("Please enter a message.")

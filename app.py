import streamlit as st
from src.pipeline.pipeline import Pipeline
from src.logger import logging

logging.info("App stating ")

st.set_page_config(page_title="Blog Search",page_icon=":mag_right:")
st.header(":blue[Agentic RAG with LangGraph:] :green[Blog Search]")

logging.info("app started")
logging.info("setting up session state for credentials")

if 'qdrant_host' not in st.session_state:
    st.session_state.qdrant_host = ""
if 'qdrant_api_key' not in st.session_state:
    st.session_state.qdrant_api_key = ""
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""

logging.info("Pipeline starting")    

run = Pipeline()
run.main()

logging.info("Run complete")
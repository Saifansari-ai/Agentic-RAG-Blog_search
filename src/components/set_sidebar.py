from src.logger import logging
from src.exception import MyException
import sys
import streamlit as st

class SetSidebar:
    """
    Setup sidebar for API keys and Configurations
    """
    logging.info("Setting Up sidebar for API keys and Configurations")
    def __init__(self):
        pass

    def set_sidebar(self):
        try:
            with st.sidebar:
                st.subheader("API Configuration")
                logging.info("Sidebar created")

                qdrant_host = st.text_input("Enter your Qdrant host URL:", type="password")
                qdrant_api_key = st.text_input("Enter your Qdrant API key:",type="password")
                gemini_api_key = st.text_input("Enter you Gemini API key:",type="password")

                if st.button("Done"):
                    if qdrant_host and qdrant_api_key and gemini_api_key:
                        st.session_state.qdrant_host = qdrant_host
                        st.session_state.qdrant_api_key = qdrant_api_key
                        st.session_state.qemini_api_key = gemini_api_key
                        st.success("API keys saved")
                    else:
                        st.warning("Please fill all the API Keys")
        except Exception as e:
            raise MyException(e,sys) from e

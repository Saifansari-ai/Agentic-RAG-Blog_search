from src.logger import logging
import streamlit as st
from src.components.set_sidebar import SetSidebar
from src.components.initialise_component import InitChomp

class Pipeline:
    """ Run all the components"""

    def __init__(self):
        pass

    def main(self):
        setup = SetSidebar()
        setup.set_sidebar()

        if not all([st.session_state.qdrant_host,
                    st.session_state.qdrant_api_key,
                    st.session_state.gemini_api_key]):
                st.warning("Please configure your API keys in the sidebar first")
                return
        
        logging.info("components initialisaion start")

        embedding_model, client, db = InitChomp.initialise(self)
        if not all([embedding_model,client,db]):
             return

        logging.info("components initialisation done ")
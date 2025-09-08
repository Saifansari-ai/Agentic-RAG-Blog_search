from src.logger import logging
from src.exception import MyException
import sys
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

class InitChomp:
    """It initialises the components of the project that requires APIs """
    def __init__(self):
        pass

    def initialise(self):
        try:
            logging.info("API initialisation start")
            if not all([st.session_state.qdrant_host,
                    st.session_state.qdrant_api_key,
                    st.session_state.gemini_api_key]):
                return None,None,None
            
            try:
                embedding_model = GoogleGenerativeAIEmbeddings(
                    model = "models/embedding-001",
                    google_api_key=st.session_state.gemini_api_key
                )

                client = QdrantClient(
                    st.session_state.qdrant_host,
                    api_key=st.session_state.qdrant_api_key
                )

                db = QdrantVectorStore(
                    client=client,
                    collection_name="qdrant_db",
                    embedding=embedding_model
                )

                logging.info("Initialisation of components done")

                return embedding_model, client, db
            except Exception as e:
                st.error(f"Initialisation error: {str(e)}")
                return None, None, None
                         
        except Exception as e:
            raise MyException(e,sys) from e
        

        

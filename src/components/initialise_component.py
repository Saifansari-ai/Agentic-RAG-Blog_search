from src.logger import logging
from src.exception import MyException
import sys
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import asyncio

class InitChomp:
    """It initialises the components of the project that requires APIs """
    def __init__(self):
        pass

    def initialise(self):
        
        logging.info("API initialisation start")
        if not all([st.session_state.qdrant_host,
                st.session_state.qdrant_api_key,
                st.session_state.gemini_api_key]):
            return None,None,None
        
        try:
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            embedding_model = GoogleGenerativeAIEmbeddings(
                model = "gemini-embedding-001",
                google_api_key=st.session_state.gemini_api_key
            )

            client = QdrantClient(
                st.session_state.qdrant_host,
                api_key=st.session_state.qdrant_api_key
            )

            # Create collection only if it doesn't exist
            if "qdrant_db" not in [c.name for c in client.get_collections().collections]:
                client.create_collection(
                    collection_name="qdrant_db",
                    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
                )

            db = QdrantVectorStore(
                client=client,
                collection_name="qdrant_db",
                embedding=embedding_model
            )

            logging.info("Initialisation of components done")

            return embedding_model, client, db
        except Exception as e:
            raise MyException(e,sys) from e
                    
                         
        
        

        

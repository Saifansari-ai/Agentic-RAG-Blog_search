from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
import streamlit as st
from src.logger import logging
from src.exception import MyException
import sys

class AddDoc:
    def __init__(self):
        pass
    
    def add_documents_to_qdrant(self,url, db):
        try:
            logging.info("Document loading")
            docs = WebBaseLoader(url).load()
            print(f"{docs} + 3")
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=200, chunk_overlap=50
            )
            doc_chunks = text_splitter.split_documents(docs)
            uuids = [str(uuid4()) for _ in range(len(doc_chunks))]
            print(f"{doc_chunks} + 8")
            # BATCH_SIZE = 2
            # for i in range(0, len(doc_chunks), BATCH_SIZE):
            #     batch = doc_chunks[i:i+BATCH_SIZE]
            #     batch_ids = uuids[i:i+BATCH_SIZE]
            db.add_documents(documents=doc_chunks, ids=uuids)
            logging.info("document parsing complete")
            return True
        except Exception as e:
            raise MyException(e,sys) from e

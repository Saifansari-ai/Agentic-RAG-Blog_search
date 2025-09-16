from src.logger import logging
from src.exception import MyException
import sys
import streamlit as st
from src.components.set_sidebar import SetSidebar
from src.components.initialise_component import InitChomp
from src.components.get_graph import GetGraph
from langchain.tools.retriever import create_retriever_tool
from src.components.generate_message import GenMessage
from langchain_core.messages import HumanMessage
from src.components.add_doc_to_qdrant import AddDoc

class Pipeline:
    """ Run all the components"""

    def __init__(self):
        pass

    def main(self):
        try:
            logging.info("main function starting")
            setup = SetSidebar()
            setup.set_sidebar()

            logging.info("Checking for session state")
            if not all([st.session_state.qdrant_host,
                        st.session_state.qdrant_api_key,
                        st.session_state.gemini_api_key]):
                    st.warning("Please configure your API keys in the sidebar first")
                    return
            
            logging.info("Session credentials exist")
            logging.info("components initialisaion start")

            inti = InitChomp()
            embedding_model, client, db = inti.initialise()
            if not all([embedding_model, client, db]):
                st.warning("error in initialisation of the components")
                return 

            logging.info("Initialisation done")

            logging.info("Retriever tools setup")
            retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5})
            retriever_tool = create_retriever_tool(
                retriever,
                "retrieve_blog_posts",
                "Search and return information about blog posts"
            )
            tools = [retriever_tool]

            logging.info("URL link setup")
            url = st.text_input(
                ":link: Paste the blog link:",
                placeholder="e.g., https://lilianweng.github.io/posts/2023-06-23-agent/"
            )
            if st.button("Enter URL"):
                if url:
                    with st.spinner("Processing documents..."):
                        add_docs = AddDoc()
                        if add_docs.add_documents_to_qdrant(url, db):
                            st.success("Documents added successfully!")
                        else:
                            st.error("Failed to add documents")
                else:
                    st.warning("Please enter a URL")

            logging.info("Getgraph funtion starting")
            Graph = GetGraph()
            graph = Graph.get_graph(retriever_tool=retriever_tool)
            query = st.text_area(
                ":bulb: Enter your query about the blog post:",
                placeholder="e.g., What does Lilian Weng say about the types of agent memory?"
            )

            if st.button("Submit Query"):
                if not query:
                    st.warning("Please enter a query")
                    return
                
                inputs = {"messages": [HumanMessage(content=query)]}
                with st.spinner("Generating response..."):
                    
                    res = GenMessage()
                    response = res.generate_message(graph, inputs)
                    st.write(response)
                   
        except Exception as e:
            raise MyException(e,sys) from e

    st.markdown("---")

    if __name__ == "__main__":
        main()
from src.logger import logging
from src.exception import MyException
import sys
from typing import Annotated, Sequence, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain import hub
from functools import partial
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def grade_documents(state) -> Literal["generate", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    print("---CHECK RELEVANCE---")

    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    model = ChatGoogleGenerativeAI(api_key=st.session_state.gemini_api_key,temperature=0,model="gemini-2.5-flash")

    llm_with_tool = model.with_structured_output(grade)

    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question":question, "context":docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "generate"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return "rewrite"
    
def agent(state, tools):
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """

    print("--CALL-AGENT--")
    messages = state["messages"]
    print(f"{messages} + 11")

    model = ChatGoogleGenerativeAI(api_key=st.session_state.gemini_api_key,temperature=0,model="gemini-2.5-flash")

    model = model.bind_tools(tools)

    response = model.invoke(messages)
    print(f"{response} = 12")

    return {"messages":[response]}

def rewrite(state):
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f""" \n 
                    Look at the input and try to reason about the underlying semantic intent / meaning. \n 
                    Here is the initial question:
                    \n ------- \n
                    {question} 
                    \n ------- \n
                    Formulate an improved question: """,
        )
    ]

    # Grader
    model = ChatGoogleGenerativeAI(api_key=st.session_state.gemini_api_key,temperature=0,model="gemini-2.5-flash")
    response = model.invoke(msg)
    return {"messages": [response]}

def generate(state):
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with re-phrased question
    """
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content
    print(f"{docs} + 13")

    
    prompt_template = hub.pull("rlm/rag-prompt")

    
    chat_model = ChatGoogleGenerativeAI(api_key=st.session_state.gemini_api_key,temperature=0,model="gemini-2.5-flash")

    
    output_parser = StrOutputParser()
    
    
    rag_chain = prompt_template | chat_model | output_parser

    response = rag_chain.invoke({"context": docs, "question": question})
    
    return {"messages": [response]}


class GetGraph:
    
    def __init__(self):
        pass

    def get_graph(self,retriever_tool):
        try:
            logging.info("tool creating done")
            tools = [retriever_tool] 
            
            logging.info("creating new workflow")
            workflow = StateGraph(AgentState)
            
            logging.info("Adding new agent node in workflow")
            workflow.add_node("agent", partial(agent, tools=tools))
            
            logging.info("Adding tools, retriever, rewrite and genrate node to workflow")
            retrieve = ToolNode(tools)
            workflow.add_node("retrieve", retrieve)
            workflow.add_node("rewrite", rewrite)  
            workflow.add_node("generate", generate)  
            
            logging.info("Adding edges to the workflow")
            workflow.add_edge(START, "agent")

            
            workflow.add_conditional_edges(
                "agent",
                
                tools_condition,
                {
                    
                    "tools": "retrieve",
                    END: "generate",
                },
            )

            
            workflow.add_conditional_edges(
                "retrieve",
                
                grade_documents,
            )
            workflow.add_edge("generate", END)
            workflow.add_edge("rewrite", "agent")

            
            graph = workflow.compile()

            return graph
        except Exception as e:
            raise MyException(e,sys) from e

            
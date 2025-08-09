import os
import uuid
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, AnyMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.types import Command
from langchain_together import ChatTogether
from src.prompts.agents_prompts import HOTEL_AGENT_PROMPT
from src.tools.hotels_tools import get_hotel_offers ,search_hotels , tavily_search_tool
from src.utils.help import *
from langchain_groq import ChatGroq
from src.utils.help import ChatOpenRouter
from src.agents.agent_utils import Assistant , State
load_dotenv()
model_id = os.environ.get("HOTEL_AGENT_MODEL_ID")

tools = [
    get_hotel_offers ,search_hotels , tavily_search_tool
]
 

llm = ChatTogether(model_name=model_id , temperature=0.8 , max_tokens=8000)
assistant_runnable = HOTEL_AGENT_PROMPT | llm.bind_tools(tools)


    
    
    

hotel_builder = StateGraph(State)
hotel_builder.add_node("assistant", Assistant(assistant_runnable))
hotel_builder.add_node("tools", create_tool_node_with_fallback(tools))

hotel_builder.add_edge(START, "assistant")

hotel_builder.add_conditional_edges(
    "assistant",
    tools_condition, 
)

hotel_builder.add_edge("tools", "assistant")
hotel_builder.set_finish_point("assistant")

memory = InMemorySaver()
hotel_graph = hotel_builder.compile(checkpointer=memory)


def hotel_node(state:State) : 
    results = hotel_graph.invoke(state) 
    return Command(
        update={
            "messages" : state["messages"] + [
                AIMessage(content=results["messages"][-1].content , name="hotel_node")
            ]
        } , 
        goto="supervisor"
    )


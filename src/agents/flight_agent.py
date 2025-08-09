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
from src.prompts.agents_prompts import FLIGHT_AGENT_PROMPT
from src.tools.search_flights import get_airport_name_from_iata , get_nearby_airports ,search_flight , book_flight_manually,get_checkin_links,check_flight_status 
from src.utils.help import *
from langchain_groq import ChatGroq
from src.utils.help import ChatOpenRouter
from src.agents.agent_utils import State , Assistant
load_dotenv()
model_id = os.environ.get("FLIGHT_AGENT_MODEL_ID")

tools = [
    get_airport_name_from_iata , get_nearby_airports ,search_flight , book_flight_manually,get_checkin_links,check_flight_status
]



llm = ChatTogether(model_name=model_id , temperature=0.8 , max_tokens=8000)
assistant_runnable = FLIGHT_AGENT_PROMPT | llm.bind_tools(tools)

flight_builder = StateGraph(State)
flight_builder.add_node("assistant", Assistant(assistant_runnable))
flight_builder.add_node("tools", create_tool_node_with_fallback(tools))

flight_builder.add_edge(START, "assistant")

flight_builder.add_conditional_edges(
    "assistant",
    tools_condition, 
)

flight_builder.add_edge("tools", "assistant")
flight_builder.set_finish_point("assistant")

memory = InMemorySaver()
flight_graph = flight_builder.compile(checkpointer=memory)

thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": thread_id
    }
}


def flight_node(state:State) : 
    results = flight_graph.invoke(state ) 
    return Command(
        update={
            "messages" : state["messages"] + [
                AIMessage(content=results["messages"][-1].content , name="flight_node")
            ]
        } , 
        goto="supervisor"
    )


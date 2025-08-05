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
from src.prompts.agents_prompts import DIESTINATION_AGENT_PROMPT
from src.tools.destination_tools import get_tours_and_activities , city_search_amadeus , tavily_search_tool ,get_city_coordinates  , get_user_location
from src.utils.help import *
from langchain_groq import ChatGroq
from src.utils.help import ChatOpenRouter
from agent_utils import Assistant , State
load_dotenv()
model_id = os.environ.get("HOTEL_AGENT_MODEL_ID")

tools = [
    get_tours_and_activities , city_search_amadeus , tavily_search_tool ,get_city_coordinates , get_user_location
]
 

# LLM
llm = ChatTogether(model_name=model_id , temperature=0.8)
assistant_runnable = DIESTINATION_AGENT_PROMPT | llm.bind_tools(tools)



# Build the LangGraph
destination_builder = StateGraph(State)
destination_builder.add_node("assistant", Assistant(assistant_runnable))
destination_builder.add_node("tools", create_tool_node_with_fallback(tools))

destination_builder.add_edge(START, "assistant")

# Direct based on whether tools were requested
destination_builder.add_conditional_edges(
    "assistant",
    tools_condition, 
)

destination_builder.add_edge("tools", "assistant")
destination_builder.set_finish_point("assistant")

# Compile graph
memory = InMemorySaver()
destination_graph = destination_builder.compile(checkpointer=memory)


def destination_node(state:State) : 
    results = destination_graph.invoke(state) 
    print(results)
    return Command(
        update={
            "messages" : state["messages"] + [
                AIMessage(content=results["messages"][-1].content , name="destination_node")
            ]
        } , 
        goto="supervisor"
    )

thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": thread_id
    }
}
""" print("🛫 Welcome to the Destination Agent! Type 'quit' to exit.\n")
_printed = set()
while True:
     user_input = input("user: > ")
     if user_input.lower() == "quit":
         print("Session ended.")
         break

     events = destination_graph.stream(
         {"messages": [HumanMessage(content=user_input)]},
         config=config ,
         stream_mode="values"
     )

     for event in events:
         print(event)
         print_event(event, _printed) 
         """
        


 
 

from src.prompts.agents_prompts import COORDINATOR_AGENT_PROMPT
from typing_extensions import TypedDict, Annotated, Literal
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.types import Command
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os
from langgraph.graph import START, END, StateGraph
from src.agents.flight_agent import flight_node
from src.agents.hotels_agent import hotel_node
from src.agents.destination_agent import destination_node
from src.utils.help import print_event
from langgraph.checkpoint.memory import InMemorySaver
import uuid
from src.utils.help import ChatOpenRouter

load_dotenv()
model_id = os.environ.get("HOTEL_AGENT_MODEL_ID")
llm = ChatTogether(model_name=model_id, temperature=0.85 , max_tokens=8000)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    next: str
    cur_reasoning: str
    query: str

class Router(TypedDict):
    next: Annotated[Literal["flight_agent", "hotel_agent", "destination_agent", "FINISH"], "worker to route to next, or FINISH"]
    reasoning: Annotated[str, "Support proper reasoning for routing to the worker"]

def supervisor_node(state: State) -> Command:
    messages = [SystemMessage(content=COORDINATOR_AGENT_PROMPT)]
    
    if state.get("messages"):
        messages.extend(state["messages"])
    
    # Try to extract the latest query
    query = state.get("query", "")
    if not query and state.get("messages"):
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                query = msg.content
                break
    
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    
    
    print(response)
    if goto == "FINISH":
        goto = END
    
    return Command(
        goto=goto,
        update={
            "next": response["next"],
            "cur_reasoning": response["reasoning"],
            "query": query
        }
    )

builder = StateGraph(State)

builder.add_node("supervisor", supervisor_node)
builder.add_node("flight_agent", flight_node)
builder.add_node("hotel_agent", hotel_node)
builder.add_node("destination_agent", destination_node)  # Added destination agent node

builder.set_entry_point("supervisor")

builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next"],
    {
        "flight_agent": "flight_agent",
        "hotel_agent": "hotel_agent",
        "destination_agent": "destination_agent",  
        "FINISH": END
    }
)

builder.add_edge("flight_agent", "supervisor")
builder.add_edge("hotel_agent", "supervisor")
builder.add_edge("destination_agent", "supervisor")  # Added destination agent return edge

memory = InMemorySaver()

final_graph = builder.compile(checkpointer=memory)


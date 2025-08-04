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
from src.utils.help import print_event
from langgraph.checkpoint.memory import InMemorySaver
import uuid
from src.utils.help import ChatOpenRouter

load_dotenv()
model_id = os.environ.get("HOTEL_AGENT_MODEL_ID")
llm = ChatTogether(model_name=model_id , temperature=0.8)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    next: str
    cur_reasoning: str  
    query: str

# ---- Define router schema ---- #
class Router(TypedDict):
    next: Annotated[Literal["flight_agent", "hotel_agent", "FINISH"], "worker to route to next, or FINISH"]
    reasoning: Annotated[str, "Support proper reasoning for routing to the worker"]

# ---- Supervisor Node ---- #
def supervisor_node(state: State) -> Command:
    # Get all messages or at least the conversation context
    messages = [SystemMessage(content=COORDINATOR_AGENT_PROMPT)]
    
    # Include more context, not just the last message
    if state.get("messages"):
        messages.extend(state["messages"])
    
    # Try to extract the latest query
    query = state.get("query", "")
    if not query and state.get("messages"):
        # Get the most recent human message
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                query = msg.content
                break
    
    # LLM-based routing
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    
    
    print("================================= response ===============")
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

# ---- LangGraph Building ---- #
builder = StateGraph(State)
builder.add_node("supervisor", supervisor_node)
builder.add_node("flight_agent", flight_node)
builder.add_node("hotel_agent", hotel_node)

# Set entry point
builder.set_entry_point("supervisor")

# Add conditional edges from supervisor based on routing decision
builder.add_conditional_edges(
    "supervisor",
    lambda state: state["next"],  # This should return the routing decision
    {
        "flight_agent": "flight_agent",
        "hotel_agent": "hotel_agent", 
        "FINISH": END
    }
)

# Add edges back to supervisor after agent completion
builder.add_edge("flight_agent", "supervisor")
builder.add_edge("hotel_agent", "supervisor")

# ---- Compile Graph ---- #
memory = InMemorySaver()
final_graph = builder.compile(checkpointer=memory)

# ---- Runtime ---- #
thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

print("🛫 Welcome to the Booking Agent! Type 'quit' to exit.\n")
_printed = set()

while True:
    user_input = input("user: > ")
    if user_input.lower() == "quit":
        print("Session ended.")
        break
    
    try:
        events = final_graph.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="values"
        )
        
        for event in events:
            print_event(event, _printed)
            
    except Exception as e:
        print(f"Error: {e}")
        print("Please try again.")
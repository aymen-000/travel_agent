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

from langchain_together import ChatTogether
from src.prompts.agents_prompts import FLIGHT_AGENT_PROMPT
from src.tools.search_flights import (
    search_flight,
    check_flight_status,
    get_checkin_links,
    get_airport_name_from_iata,
    get_nearby_airports,
    book_flight_manually,
)
from src.utils.help import *


# Load environment
load_dotenv()
model_id = os.environ.get("FLIGHT_AGENT_MODEL_ID")

# Define tools
tools = [
    search_flight,
    check_flight_status,
    get_checkin_links,
    get_airport_name_from_iata,
    get_nearby_airports,
    book_flight_manually,
]

# Define state
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# LLM
llm = ChatTogether(model=model_id, temperature=1)
assistant_runnable = FLIGHT_AGENT_PROMPT | llm.bind_tools(tools)



# Assistant wrapper with retry logic
class Assistant:
    def __init__(self, runnable: Runnable):
        self.run = runnable

    def __call__(self, state: State, config=RunnableConfig):
        while True:
            results = self.run.invoke(state)

            # Check if assistant returned valid output
            if not results.tool_calls and (
                not results.content
                or (isinstance(results.content, list) and not results.content[0].get("text"))
            ):
                message = state["messages"] + [HumanMessage(content="Respond with a real output")]
                state = {**state, "messages": message}
            else:
                break

        return {"messages": [results]}


# Build the LangGraph
builder = StateGraph(State)
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))

builder.add_edge(START, "assistant")

# Direct based on whether tools were requested
builder.add_conditional_edges(
    "assistant",
    tools_condition, 
)

builder.add_edge("tools", "assistant")
builder.set_finish_point("assistant")

# Compile graph
memory = InMemorySaver()
part_1_graph = builder.compile(checkpointer=memory)

# Runtime loop
thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

_printed = set()
print("🛫 Welcome to the Flight Agent! Type 'quit' to exit.\n")

while True:
    user_input = input("user: > ")
    if user_input.lower() == "quit":
        print("Session ended.")
        break

    events = part_1_graph.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config=config,
        stream_mode="values"
    )

    for event in events:
        print(event)
        print_event(event, _printed)

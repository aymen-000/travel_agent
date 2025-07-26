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
from src.prompts.agents_prompts import HOTEL_AGENT_PROMPT
from src.tools.hotels_tools import get_hotel_offers ,search_hotels , tavily_search_tool
from src.utils.help import *
 
load_dotenv()
model_id = os.environ.get("HOTEL_AGENT_MODEL_ID")

tools = [
    get_hotel_offers ,search_hotels , tavily_search_tool
]
 

 # Define state
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# LLM
llm = ChatTogether(model=model_id, temperature=1)
assistant_runnable = HOTEL_AGENT_PROMPT | llm.bind_tools(tools)


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
hotel_builder = StateGraph(State)
hotel_builder.add_node("assistant", Assistant(assistant_runnable))
hotel_builder.add_node("tools", create_tool_node_with_fallback(tools))

hotel_builder.add_edge(START, "assistant")

# Direct based on whether tools were requested
hotel_builder.add_conditional_edges(
    "assistant",
    tools_condition, 
)

hotel_builder.add_edge("tools", "assistant")
hotel_builder.set_finish_point("assistant")

# Compile graph
memory = InMemorySaver()
part_1_graph = hotel_builder.compile(checkpointer=memory)

# Runtime loop
thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

print("🛫 Welcome to the Hotel Agent! Type 'quit' to exit.\n")
_printed = set()
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
        
        


 
 

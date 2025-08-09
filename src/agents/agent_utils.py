from typing import TypedDict  , Annotated  
from langchain_core.messages import HumanMessage , AnyMessage
from langchain_core.runnables import Runnable  , RunnableConfig
from langgraph.graph.message import add_messages 
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


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
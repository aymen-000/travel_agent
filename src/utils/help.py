import requests
import os 
import sys 
from dotenv import load_dotenv 
from typing import Dict , List
from langchain_core.messages import ToolMessage 
from langgraph.prebuilt import ToolNode
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables import RunnableLambda


load_dotenv() 
def get_amadeus_token() -> str:
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AMADEUS_CLIENT_ID"),
        "client_secret": os.getenv("AMADEUS_CLIENT_SECRET"),
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]




def handle_tool_error(state) -> Dict  : 
    """Function to handle errors that accur during tool execution.

    Args:
        state (dict): The current state of the AI agent , which includes messgaes and tool calls 

    Returns:
        Dict: A dicitionary containing error messgaes for each tool that encountered an issue.  
    """
    
    error = state.get("error") 
    tool_calls = state["messages"][-1].tool_calls 
    
    
    return {
        "messages" : [
            ToolMessage(
                content=f"Error : {repr(error)} \n please fix your mistakes" , 
                tool_call_id = tc["id"]
            ) 
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools : List) -> Dict : 
    """
        Function to create a tool node with fallback error handling .
        
    Args : 
        tools (List) : A list of tools to be included in the node 
        
    Return : 
        dict : A tool node that uses fallback behavior in case of errors .
    """ 
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)] ,  exception_key="error" 
        
    )
    
    
def print_event(event: dict, _printed: set):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            print(msg_repr)
            _printed.add(message.id)
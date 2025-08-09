from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage
from src.agents.flight_agent import flight_graph
from src.agents.agent_utils import State
from langgraph.types import Command
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel


class Inputs(BaseModel) : 
    query : str  
    thread_id : str = Query(default=None) 
    
router = APIRouter()

flight_conversations = {}

@router.post("/search")
async def search_flights(inputs: Inputs):
    thread_id = inputs.thread_id
    if not thread_id:
        thread_id = str(uuid.uuid4())
        flight_conversations[thread_id] = []
    
    # Retrieve past messages for this thread
    messages = flight_conversations.get(thread_id, [])
    
    messages.append(HumanMessage(content=inputs.query))
    
    state = State(messages=messages)
    config = {
    "configurable": {
        "thread_id": thread_id
    }
    }
    result: Command = flight_graph.invoke(state , config)
    response_message = result["messages"][-1]
    
    messages.append(response_message)
    flight_conversations[thread_id] = messages
    
    return {
        "response": response_message.content,
        "agent_id": "flight",
        "thread_id": thread_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages_count": len(messages)
    }
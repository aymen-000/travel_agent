from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage
from src.agents.destination_agent import destination_graph
from src.agents.agent_utils import State
from langgraph.types import Command
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel


class Inputs(BaseModel) : 
    query : str  
    thread_id : str = Query(default=None) 
    
router = APIRouter()

destination_conversations = {}

@router.post("/search")
async def search_destinations(inputs:Inputs):
    thread_id = inputs.thread_id
    if not thread_id:
        thread_id = str(uuid.uuid4())
        destination_conversations[thread_id] = []
    
    messages = destination_conversations.get(thread_id, [])
    
    messages.append(HumanMessage(content=inputs.thread_id))
    
    state = State(messages=messages)
    
    config = {
    "configurable": {
        "thread_id": thread_id
    }
    }
    result = destination_graph.invoke(state , config=config)
    response_message = result["messages"][-1]
    
    messages.append(response_message)
    destination_conversations[thread_id] = messages
    
    return {
        "response": response_message.content,
        "agent_id": "destination_agent",
        "thread_id": thread_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages_count": len(messages)
    }

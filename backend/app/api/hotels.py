from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage
from src.agents.hotels_agent import hotel_graph
from src.agents.agent_utils import State
from langgraph.types import Command
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel


class Inputs(BaseModel) : 
    query : str  
    thread_id : str = Query(default=None) 
    
    
router = APIRouter()

# In-memory storage: {thread_id: [messages]}
hotel_conversations = {}

@router.post("/search")
async def search_hotels(input:Inputs):
    thread_id = input.thread_id
    if not thread_id:
        thread_id = str(uuid.uuid4())
        hotel_conversations[thread_id] = []
    
    messages = hotel_conversations.get(thread_id, [])
    
    messages.append(HumanMessage(content=input.query))
    
    state = State(messages=messages)
    config = {
    "configurable": {
        "thread_id": thread_id
    }
    }
    
    result = hotel_graph.invoke(state , config=config)
    response_message = result["messages"][-1]
    
    messages.append(response_message)
    hotel_conversations[thread_id] = messages
    
    return {
        "response": response_message.content,
        "agent_id": "hotel",
        "thread_id": thread_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages_count": len(messages)
    }

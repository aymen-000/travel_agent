from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage
from src.agents.team_agent import final_graph
from src.agents.agent_utils import State
from langgraph.types import Command
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel


class Inputs(BaseModel) : 
    query : str  
    thread_id : str = Query(default=None)
router = APIRouter()

# Temporary in-memory store {thread_id: [messages]}
conversations = {}

@router.post("/search")
async def search_travel(Input : Inputs):
    thread_id = Input.thread_id 
    if not thread_id:
        thread_id = str(uuid.uuid4())
        conversations[thread_id] = []
    
    messages = conversations.get(thread_id, [])
    
    messages.append(HumanMessage(content=Input.query))
    
    state = State(messages=messages)
    config = {
    "configurable": {
        "thread_id": thread_id
    }
}
    result: Command = final_graph.invoke(state  , config=config)
    response_message = result["messages"][-1]
    
    messages.append(response_message)
    
    conversations[thread_id] = messages
    
    return {
        "response": response_message.content,
        "agent_id": "team",
        "thread_id": thread_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages_count": len(messages)
    }
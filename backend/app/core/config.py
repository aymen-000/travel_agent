import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Travel Agent API"
    API_V1_STR: str = "/api/v1"
    HOTEL_AGENT_MODEL_ID: str = os.getenv("HOTEL_AGENT_MODEL_ID", "")
    FLIGHT_AGENT_MODEL_ID: str = os.getenv("HOTEL_AGENT_MODEL_ID", "")
    DESTINATION_AGENT_MODEL_ID: str = os.getenv("HOTEL_AGENT_MODEL_ID", "")
    TEAM_AGENT_MODEL_ID : str = os.getenv("HOTEL_AGENT_MODEL_ID" , "")
settings = Settings()
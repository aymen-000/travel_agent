import requests
import os 
import sys 
from dotenv import load_dotenv 


sys.path.append("../../")

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



from langchain_core.tools import tool 
from dotenv import load_dotenv 
from typing import Optional , Dict , List , Any 
from pydantic import BaseModel , Field 
import requests 
from src.utils.help import get_amadeus_token 
from duckduckgo_search import DDGS
from langchain_tavily import TavilySearch



load_dotenv()

class CitySearchInput(BaseModel):
    keyword: str = Field(description="Keyword that starts a city's name. Example: PARIS")
    countryCode: Optional[str] = Field(None, description="ISO 3166 Alpha-2 country code. Example: FR")
    max: Optional[int] = Field(3, description="Number of results to return")
    include: Optional[List[str]] = Field(default_factory=lambda: ["AIRPORTS"], description="Resources to include, e.g., AIRPORTS")

@tool
def city_search_amadeus(input: CitySearchInput) -> dict:
    """Search for cities using a keyword and optional country code, using Amadeus API."""
    token = get_amadeus_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.amadeus+json"
    }

    params = {
        "keyword": input.keyword,
        "max": input.max,
    }
    if input.countryCode:
        params["countryCode"] = input.countryCode
    if input.include:
        params["include"] = ",".join(input.include)

    response = requests.get(
        "https://test.api.amadeus.com/v1/reference-data/locations/cities",
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        return {"error": f"Amadeus API error: {response.status_code}", "details": response.json()}
    
    return response.json()["data"]


class ActivitiesInput(BaseModel):
    latitude: float = Field(..., description="Latitude in decimal degrees. Example: 41.397158")
    longitude: float = Field(..., description="Longitude in decimal degrees. Example: 2.160873")
    radius: Optional[int] = Field(1, description="Search radius in km (0-20). Default is 1.")

@tool
def get_tours_and_activities(input: ActivitiesInput) -> dict:
    """Returns tours and activities around a given location using the Amadeus API."""
    token = get_amadeus_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.amadeus+json"
    }

    params = {
        "latitude": input.latitude,
        "longitude": input.longitude,
        "radius": input.radius
    }

    response = requests.get(
        "https://test.api.amadeus.com/v1/shopping/activities",
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        return {"error": f"Amadeus API error: {response.status_code}", "details": response.json()}
    
    return response.json()["data"][:3]


@tool 
def get_city_coordinates(input: CitySearchInput)-> Dict : 
    """Search for cities using a keyword and optional country code, using Amadeus API and get it is latitude and  longitude """
    token = get_amadeus_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.amadeus+json"
    }

    params = {
        "keyword": input.keyword,
        "max": input.max,
    }
    if input.countryCode:
        params["countryCode"] = input.countryCode
    if input.include:
        params["include"] = ",".join(input.include)

    response = requests.get(
        "https://test.api.amadeus.com/v1/reference-data/locations/cities",
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        return {"error": f"Amadeus API error: {response.status_code}", "details": response.json()}
    
    return response.json()["data"][0]["geoCode"]

@tool
def get_user_location(_: dict = {}) -> Dict:
    """Gets the user's current location using their IP address."""
    try:
        response = requests.get("http://ip-api.com/json/")
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data.get("city").replace("é" , "e").upper(),
                "country": data.get("countryCode"),
            }
        else:
            return {"error": f"Failed to get location: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
    
    
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
) 


from langchain_core.tools import tool 
from dotenv import load_dotenv 
from typing import Optional, Dict , List  , Any
from pydantic import BaseModel , Field 
import requests
from src.utils.help import get_amadeus_token
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup 
from langchain_tavily import TavilySearch

load_dotenv()


class HotelSearchInput(BaseModel):
    city_code: str = Field(..., description="City IATA code, e.g., 'PAR' for Paris")
    radius: str | int = Field(description="Maximum distance from the geographical coordinates express in defined units. The default unit is metric kilometer." , default="5")
    
    
class HotelOffer(BaseModel):
    hotelids: str = Field(
        description="Amadeus property codes on 8 chars. Mandatory parameter for a search by predefined list of hotels."
    )
    adults: int = Field(default=2, description="Number of adult guests (1-9) per room.")
    checkInDate: str = Field(
        description="Check-in date in format YYYY-MM-DD. Must not be in the past."
    )
    checkOutDate: str = Field(
        description="Check-out date in format YYYY-MM-DD. Must be after checkInDate."
    )
    countryOfResidence: Optional[str] = Field(
        default=None,
        description="ISO 3166-1 code of the traveler's country of residence."
    )
    roomQuantity: int = Field(
        default=1,
        description="Number of rooms requested (1-9)."
    )
    priceRange: str = Field(
        default="200-300",
        description="Filter hotel offers by price per night interval (e.g., 200-300, -300, or 100)."
    )
    currency: str = Field(
        default="USD",
        description="Currency code in ISO 4217 format (e.g., USD, EUR)."
    )


    
@tool
def search_hotels(input_data: HotelSearchInput) -> List[dict]:
    """
    Search for hotels offers using Amadeus API. Return a list of hotels max 10
    """
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
    token = get_amadeus_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "cityCode": input_data.city_code,
        "radius": input_data.radius,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = []
    for item in response.json().get("data", []):
        result.append({
            "name": item.get("name" , "without name"),
            "geo_code" : item.get("geoCode" , "no geocode") , 
            'hotelId' : item.get("hotelId" , "no id") , 
            'address' : item.get('address'), 
            "distance" : str(item.get("distance").get("value")) +" " + item.get("distance").get("unit")
        })
        
    if len(result) > 10 : 
        return result[:10]
    
    return result


@tool
def get_hotel_offers(input_data: HotelOffer) -> List[Dict]:
    """
    Fetch hotel offers for given hotel IDs and criteria using Amadeus API.

    Args:
        input_data (HotelOffer): Filter parameters for hotel search.

    Returns:
        List[Dict]: A list of available hotel offers with details.
    """
    url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
    token = get_amadeus_token()
    headers = {"Authorization": f"Bearer {token}"}

    params : Dict[str , Any] = {
        "hotelIds": input_data.hotelids,
        "adults": input_data.adults,
        "checkInDate": input_data.checkInDate,
        "checkOutDate": input_data.checkOutDate,
        "roomQuantity": input_data.roomQuantity,
        "priceRange": input_data.priceRange,
        "currency": input_data.currency,
    }

    if input_data.countryOfResidence:
        params["countryOfResidence"] = input_data.countryOfResidence

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
    except requests.exceptions.HTTPError as http_err:
        try:
            error_json = response.json()
            print("API Error:", error_json.get("errors", [])[0].get("title", str(http_err)))
        except Exception:
            print("HTTP Error:", str(http_err))
        return []
    except Exception as e:
        print("Unexpected error:", str(e))
        return []

    data = response.json().get("data", [])
    results = []

    for hotel_offer in data:
        hotel_info = hotel_offer.get("hotel", {})
        offers = hotel_offer.get("offers", [])

        for offer in offers:
            results.append({
                "hotel_name": hotel_info.get("name"),
                "hotel_id": hotel_info.get("hotelId"),
                "city_code": hotel_info.get("cityCode"),
                "latitude": hotel_info.get("latitude"),
                "longitude": hotel_info.get("longitude"),
                "room_type": offer.get("room", {}).get("typeEstimated", {}).get("category"),
                "bed_type": offer.get("room", {}).get("typeEstimated", {}).get("bedType"),
                "description": offer.get("room", {}).get("description", {}).get("text"),
                "price_total": offer.get("price", {}).get("total"),
                "currency": offer.get("price", {}).get("currency"),
                "cancellation_policy": offer.get("policies", {}).get("cancellation", {}).get("description", {}).get("text"),
                "check_in": offer.get("checkInDate"),
                "check_out": offer.get("checkOutDate"),
                "booking_link": offer.get("self")
            })

    return results


tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
) 
from langchain_core.tools import tool
from typing import Optional, Dict
import requests
from dotenv import load_dotenv
from src.utils.help import get_amadeus_token

load_dotenv()


@tool
def search_flight(
    originLocationCode: str,  # e.g., "ALG"
    destinationLocationCode: str,  # e.g., "IST"
    departureDate: str,  # format: YYYY-MM-DD
    returnDate: Optional[str] = None,  # optional return date
    adults: int = 1,
    travelClass: Optional[str] = None  # e.g., ECONOMY, BUSINESS
) -> str:
    """
    Search for available flights between two cities using the Amadeus API.
    
    Required:
    - originLocationCode: The IATA code of the departure airport.
    - destinationLocationCode: The IATA code of the arrival airport.
    - departureDate: The date of departure (YYYY-MM-DD).
    
    Optional:
    - returnDate: The return date for round trip (YYYY-MM-DD).
    - adults: Number of adult passengers.
    - travelClass: Desired travel class (ECONOMY, BUSINESS, FIRST).
    
    Returns:
    Top 3 available flight options with price, time, stops, and airline info.
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params: Dict[str, str | int | float] = {
        "originLocationCode": originLocationCode,
        "destinationLocationCode": destinationLocationCode,
        "departureDate": departureDate,
        "adults": adults,
    }
    if returnDate:
        params["returnDate"] = returnDate
    if travelClass:
        params["travelClass"] = travelClass

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()
    if not data.get("data"):
        return "No flights found for the given criteria."

    results = []
    for i, offer in enumerate(data["data"][:3], start=1):
        itinerary = offer["itineraries"][0]
        segments = itinerary["segments"]
        departure = segments[0]["departure"]
        arrival = segments[-1]["arrival"]
        airline = segments[0]["carrierCode"]
        duration = itinerary["duration"]
        stops = len(segments) - 1
        price = offer["price"]["total"]
        currency = offer["price"]["currency"]
        flight_numbers = ", ".join(
            f"{seg['carrierCode']}{seg['number']}" for seg in segments
        )
        results.append(
            f"Flight {i}:\n"
            f"• Flight Number(s): {flight_numbers}\n"
            f"• From {departure['iataCode']} at {departure['at']}\n"
            f"• To {arrival['iataCode']} at {arrival['at']}\n"
            f"• Airline: {airline}\n"
            f"• Duration: {duration}\n"
            f"• Stops: {stops}\n"
            f"• Price: {price} {currency}\n"
        )

    return "\n".join(results)


@tool
def get_nearby_airports(
    latitude: float,
    longitude: float,
    radius: Optional[int] = 100
) -> str:
    """
    Find airports near a given location (based on latitude and longitude).
    
    Required:
    - latitude: Latitude coordinate.
    - longitude: Longitude coordinate.
    
    Optional:
    - radius: Search radius in kilometers (default is 100km).
    
    Returns:
    A list of nearby airport IATA codes, names, and distance.
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v1/reference-data/locations/airports"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"latitude": latitude, "longitude": longitude, "radius": radius}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("data"):
        return "No airports found near the provided coordinates."

    results = []
    for loc in data["data"]:
        code = loc.get("iataCode", "N/A")
        name = loc.get("name", "Unknown")
        distance = loc.get("distance", {}).get("value", "N/A")
        unit = loc.get("distance", {}).get("unit", "KM")
        results.append(f"• {code} - {name} ({distance} {unit})")

    return "\n".join(results)


@tool
def get_airport_name_from_iata(iata_code: str) -> str:
    """
    Retrieve airport name and location using its IATA code.
    
    Required:
    - iata_code: 3-letter IATA airport code (e.g., CDG, JFK).
    
    Returns:
    Full airport name and location (city and country).
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params = {"keyword": iata_code, "subType": "AIRPORT"}
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("data"):
        return f"No information found for IATA code: {iata_code}"

    loc = data["data"][0]
    name = loc.get("name", "Unknown")
    city = loc.get("address", {}).get("cityName", "Unknown")
    country = loc.get("address", {}).get("countryName", "Unknown")
    return f"{iata_code.upper()} - {name}, {city}, {country}"


@tool
def check_flight_status(flight_number: str, scheduled_date: str) -> str:
    """
    Check the status of a specific flight on a given date.
    
    Required:
    - flight_number: Airline + flight number (e.g., TK652).
    - scheduled_date: Date in YYYY-MM-DD format.
    
    Returns:
    Flight's departure and arrival details.
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/schedule/flights"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "carrierCode": flight_number[:2],
        "flightNumber": flight_number[2:],
        "scheduledDepartureDate": scheduled_date,
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get("data"):
        return f"No status found for flight {flight_number} on {scheduled_date}."

    flights = data["data"]
    result = []

    for flight in flights[:1]:
        flight_points = flight.get("flightPoints", [])
        if len(flight_points) < 2:
            continue

        dep = flight_points[0]
        arr = flight_points[1]

        dep_code = dep.get("iataCode", "Unknown")
        arr_code = arr.get("iataCode", "Unknown")

        dep_time = dep.get("departure", {}).get("timings", [{}])[0].get("value", "Unknown")
        arr_time = arr.get("arrival", {}).get("timings", [{}])[0].get("value", "Unknown")

        result.append(
            f"Flight {flight_number} on {scheduled_date}:\n"
            f"• Departure: {dep_code} at {dep_time}\n"
            f"• Arrival: {arr_code} at {arr_time}"
        )

    return "\n".join(result) if result else f"Incomplete data for {flight_number}."


@tool
def get_checkin_links(airline_code: str) -> str:
    """
    Get the official check-in URL for a specific airline.
    
    Required:
    - airline_code: 2-letter airline IATA code (e.g., TK, AF).
    
    Returns:
    Direct link to the airline's check-in page.
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/reference-data/urls/checkin-links"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"airlineCode": airline_code}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("data"):
            return f"No check-in link found for airline: {airline_code.upper()}"

        return data["data"][0].get("href", f"No link available for {airline_code.upper()}")
    except requests.exceptions.RequestException as e:
        return f"Error fetching check-in link: {str(e)}"


@tool
def book_flight_manually(
    originLocationCode: str,
    destinationLocationCode: str,
    departureDate: str,
    returnDate: Optional[str] = None,
    adults: int = 1,
    travelClass: Optional[str] = None,
) -> str:
    """
    This tool provides flight details for manual booking (not real-time booking).
    
    Required:
    - originLocationCode: IATA code of departure airport.
    - destinationLocationCode: IATA code of destination airport.
    - departureDate: Flight departure date.
    
    Optional:
    - returnDate: Return trip date.
    - adults: Number of passengers.
    - travelClass: ECONOMY, BUSINESS, etc.
    
    Returns:
    A single recommended flight with info for manual booking.
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": originLocationCode,
        "destinationLocationCode": destinationLocationCode,
        "departureDate": departureDate,
        "adults": adults,
    }

    if returnDate:
        params["returnDate"] = returnDate
    if travelClass:
        params["travelClass"] = travelClass

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()
    if not data.get("data"):
        return "No flights found for the given criteria."

    offer = data["data"][0]
    itinerary = offer["itineraries"][0]
    segments = itinerary["segments"]
    departure = segments[0]["departure"]
    arrival = segments[-1]["arrival"]
    airline = segments[0]["carrierCode"]
    flight_number = segments[0]["number"]
    duration = itinerary["duration"]
    stops = len(segments) - 1
    price = offer["price"]["total"]
    currency = offer["price"]["currency"]

    return (
        "⚠️ This tool does not support live booking.\n"
        "Here is the flight info for manual booking:\n\n"
        f"• From: {departure['iataCode']} at {departure['at']}\n"
        f"• To: {arrival['iataCode']} at {arrival['at']}\n"
        f"• Airline: {airline}\n"
        f"• Flight Number: {airline}{flight_number}\n"
        f"• Duration: {duration}\n"
        f"• Stops: {stops}\n"
        f"• Price: {price} {currency}"
    )
    
from langchain_core.tools import tool
import requests
from typing import Optional
from src.utils.help import get_amadeus_token

@tool
def get_checkin_links(
    airlineCode: str,  # e.g., "BA", "AF", "1X"
    language: Optional[str] = "en-GB"  # e.g., "EN", "en-GB"
) -> str:
    """
    Get online check-in links (web and mobile) for a specific airline using its IATA or ICAO code.

    Required:
    - airlineCode: 2-letter or 3-letter airline code (e.g., BA, AF, TK).

    Optional:
    - language: Language code for the check-in page, e.g., "EN", "en-GB". Defaults to "en-GB".

    Returns:
    Direct check-in URLs (web & mobile) for the airline, or an appropriate message if unavailable.
    """
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/reference-data/urls/checkin-links"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "airlineCode": airlineCode,
        "language": language
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("data"):
            return f"No check-in links found for airline: {airlineCode.upper()}"

        links = []
        for entry in data["data"]:
            channel = entry.get("channel", "Unknown")
            href = entry.get("href", "No URL")
            links.append(f"• {channel} Check-in: {href}")

        return f"✈️ Online Check-in Links for {airlineCode.upper()}:\n" + "\n".join(links)

    except requests.exceptions.RequestException as e:
        return f"❌ Error fetching check-in link: {str(e)}"



result = get_checkin_links.invoke({"airlineCode" : "BA", "language" :"EN"})



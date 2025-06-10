from langchain_core.tools import tool
from typing import Optional, Dict
import sys

sys.path.append("../../")  # set the path to root
import requests
from dotenv import load_dotenv
import os

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


@tool
def search_flight(
    originLocationCode: str,
    destinationLocationCode: str,
    departureDate: str,
    returnDate: Optional[str] = None,
    adults: int = 1,
    travelClass: Optional[str] = None,
) -> str:
    """Searches for available flights between two cities using the Amadeus API.
    Returns flight number, airline, stops, duration, and price."""

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
    latitude: float, longitude: float, radius: Optional[int] = 100
) -> str:
    """
    Finds nearby airports using latitude and longitude. Radius is in kilometers (default: 100km).
    Returns a list of airport IATA codes and names.
    """

    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v1/reference-data/locations/airports"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, str | int | float | None] = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
    }

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
    """Returns full airport name and location from IATA code."""
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v1/reference-data/locations"
    params: Dict[str, str] = {"keyword": iata_code, "subType": "AIRPORT"}
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
    """Returns scheduled flight status from flight number and date (YYYY-MM-DD)."""
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/schedule/flights"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, str] = {
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

        dep_point = flight_points[0]
        arr_point = flight_points[1]

        dep_code = dep_point.get("iataCode", "Unknown")
        arr_code = arr_point.get("iataCode", "Unknown")

        dep_time = (
            dep_point.get("departure", {})
            .get("timings", [{}])[0]
            .get("value", "Unknown")
        )
        arr_time = (
            arr_point.get("arrival", {}).get("timings", [{}])[0].get("value", "Unknown")
        )

        result.append(
            f"Flight {flight_number} on {scheduled_date}:\n"
            f"Departure: {dep_code} at {dep_time}\n"
            f"Arrival: {arr_code} at {arr_time}"
        )

    return (
        "\n".join(result)
        if result
        else f"Incomplete flight data for {flight_number} on {scheduled_date}."
    )


@tool
def get_checkin_links(airline_code: str) -> str:
    """Returns the check-in links for a specific airline using its IATA code (e.g., 'LH', 'AF')."""
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/reference-data/urls/checkin-links"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, str] = {"airlineCode": airline_code}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("data") or len(data["data"]) == 0:
            return f"No check-in link provided for airline: {airline_code.upper()}"

        return data["data"][0].get(
            "href", f"No check-in link available for {airline_code.upper()}"
        )

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
    This tool cannot book flights, but it returns flight info to help users book manually.
    """

    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    params: Dict[str, str | int] = {
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

    offer = data["data"][0]  # Just take the first one
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

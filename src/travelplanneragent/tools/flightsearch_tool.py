from crewai.tools import BaseTool
from serpapi import GoogleSearch

from dotenv import load_dotenv
import os

load_dotenv()

AIRPORT_CODES = {
    # India
    "Delhi": "DEL",
    "Mumbai": "BOM",
    "Bangalore": "BLR",
    "Hyderabad": "HYD",
    "Chennai": "MAA",
    "Kolkata": "CCU",
    "Pune": "PNQ",
    "Ahmedabad": "AMD",
    "Kochi": "COK",
    "Indore": "IDR",
    "Bhopal": "BHO",
    "Goa": "GOI",
    "Jaipur": "JAI",
    "Lucknow": "LKO",
    "Visakhapatnam": "VTZ",
    "Patna": "PAT",

    # International
    "Bali": "DPS",
    "Singapore": "SIN",
    "Dubai": "DXB",
    "London": "LHR",
    "Paris": "CDG",
    "Tokyo": "HND",
    "Bangkok": "BKK",
    "Sydney": "SYD",
    "New York": "JFK",
    "Los Angeles": "LAX",
    "Toronto": "YYZ",
    "Amsterdam": "AMS",
    "Frankfurt": "FRA",
    "Hong Kong": "HKG"
}

class FlightSearchTool(BaseTool):

    name: str = "Flight Search Tool"

    description: str = (
        "Searches Google Flights and returns the best flight options."
    )

    def _run(
        self,
        origin_city: str,
        destination_city: str,
        departure_date: str,
        number_of_adults: int = 1,
    ) -> str:
        
        origin_city = origin_city.strip().title() 
        destination_city = destination_city.strip().title()

        departure_airport_code = AIRPORT_CODES.get(origin_city) 
        arrival_airport_code = AIRPORT_CODES.get(destination_city)
        
        if not departure_airport_code:
            return f"Airport code not found for city: {origin_city}" 
        
        if not arrival_airport_code:
            return f"Airport code not found for city: {destination_city}"

        params = {
            "engine": "google_flights",
            "departure_id": departure_airport_code,
            "arrival_id": arrival_airport_code,
            "outbound_date": departure_date,
            "currency": "INR",
            "adults": number_of_adults,
            "type": "2",
            "hl": "en",
            "api_key": os.getenv("SERPAPI_API_KEY")
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        print(results)

        best_flights = results.get("best_flights", [])

        if not best_flights:
            return "No flights found."

        output = []

        for flight in best_flights[:5]:

            output.append(
                f"""
Airline: {(flight.get("flights", [{}])[0].get("airline", "Unknown"))}
Price: ₹{flight.get('price', 'N/A')}
Duration: {flight.get('total_duration', 'N/A')} mins
Flight Number: {(flight.get("flights", [{}])[0].get("flight_number", "N/A"))}
Route: {origin_city} ({departure_airport_code}) → {destination_city} ({arrival_airport_code})
Departure Time: {(flight.get("flights", [{}])[0].get("departure_airport", {}).get("time", "N/A"))}
Arrival Time: {(flight.get("flights", [{}])[0].get("arrival_airport", {}).get("time", "N/A"))}
"""
            )

        return "\n------------------\n".join(output)



#if __name__ == "__main__":
#
#    tool = FlightSearchTool()
#
#    result = tool._run(
#        origin_city="Delhi",
#        destination_city="Bali",
#        departure_date="2026-06-15",
#        number_of_adults=2
#    )
#
#    print(result)
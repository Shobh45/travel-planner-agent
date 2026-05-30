import os

from crewai.tools import BaseTool
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()


class HotelSearchTool(BaseTool):

    name: str = "Hotel Search Tool"

    description: str = (
        "Searches Google Hotels and returns the best hotel "
        "recommendations for a destination."
    )

    def _run(
        self,
        destination: str,
        check_in_date: str,
        check_out_date: str,
        adults: int = 2
    ) -> str:

        params = {
            "engine": "google_hotels",
            "q": destination,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": adults,
            "children": 0,
            "currency": "INR",
            "gl": "in",
            "hl": "en",
            "api_key": os.getenv("SERPAPI_API_KEY")
        }

        try:

            search = GoogleSearch(params)
            results = search.get_dict()

            properties = results.get("properties", [])

            if not properties:
                return (
                    f"No hotels found in {destination}"
                )

            hotel_output = []

            for hotel in properties[:5]:

                name = hotel.get(
                    "name",
                    "Unknown Hotel"
                )

                rating = hotel.get(
                    "overall_rating",
                    "N/A"
                )

                reviews = hotel.get(
                    "reviews",
                    "N/A"
                )

                nightly_price = (
                    hotel.get(
                        "rate_per_night",
                        {}
                    ).get(
                        "extracted_lowest",
                        "N/A"
                    )
                )

                check_in_time = hotel.get(
                    "check_in_time",
                    "N/A"
                )

                check_out_time = hotel.get(
                    "check_out_time",
                    "N/A"
                )

                amenities = hotel.get(
                    "amenities",
                    []
                )

                top_amenities = (
                    ", ".join(amenities[:5])
                    if amenities
                    else "Not Available"
                )

                nearby_places = hotel.get(
                    "nearby_places",
                    []
                )

                nearest_place = (
                    nearby_places[0]["name"]
                    if nearby_places
                    else "N/A"
                )

                hotel_output.append(
                    f"""
Hotel: {name}
Rating: {rating}/5
Reviews: {reviews}
Price Per Night: ₹{nightly_price}
Check-in: {check_in_time}
Check-out: {check_out_time}
Nearby Landmark: {nearest_place}
Amenities: {top_amenities}
"""
                )

            return (
                "\n----------------------------\n"
                .join(hotel_output)
            )

        except Exception as e:

            return (
                f"Error searching hotels: {str(e)}"
            )
        
    
#if __name__ == "__main__":
#    tool = HotelSearchTool()
#
#    result = tool._run(
#        destination="Delhi",
#        check_in_date="2026-06-15",
#        check_out_date="2026-06-20",
#        adults=2
#    )
#
#    print(result)
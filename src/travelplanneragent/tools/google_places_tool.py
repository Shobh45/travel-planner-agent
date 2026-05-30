import os
import requests

from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()


class GooglePlacesTool(BaseTool):

    name: str = "Google Places Search Tool"

    description: str = (
        "Searches Google Places for attractions, restaurants, hotels, and landmarks."
    )

    def _run(
        self,
        query: str
    ) -> str:

        api_key = os.getenv(
            "GOOGLE_PLACES_API_KEY"
        )

        url = (
            "https://places.googleapis.com/v1/places:searchText"
        )

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask":
                "places.displayName,"
                "places.formattedAddress,"
                "places.rating,"
                "places.userRatingCount"
        }

        payload = {
            "textQuery": query
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        places = data.get(
            "places",
            []
        )

        if not places:
            return "No places found."

        output = []

        for place in places[:5]:

            name = (
                place.get(
                    "displayName",
                    {}
                ).get(
                    "text",
                    "Unknown"
                )
            )

            address = place.get(
                "formattedAddress",
                "N/A"
            )

            rating = place.get(
                "rating",
                "N/A"
            )

            reviews = place.get(
                "userRatingCount",
                "N/A"
            )

            output.append(
                f"""
Name: {name}
Address: {address}
Rating: {rating}
Review Count: {reviews}
"""
            )

        return (
            "\n------------------\n"
            .join(output)
        )
    
if __name__ == "__main__":
    
    tool = GooglePlacesTool()

    result = tool._run(
        "Top tourist attractions in Bali"
    )

    print(result)
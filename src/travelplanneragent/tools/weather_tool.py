import requests
import os

from crewai.tools import BaseTool


class WeatherTool(BaseTool):
    name: str = "Weather Information Tool"
    description: str = (
        "Fetches real-time weather information for a given city."
    )

    def _run(self, city: str) -> str:

        api_key = os.getenv("OPENWEATHER_API_KEY")

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        response = requests.get(url)

        data = response.json()

        if response.status_code != 200:
            return f"Weather data not found for {city}"

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return (
            f"Current weather in {city}: "
            f"{weather}, temperature {temp}°C, "
            f"humidity {humidity}%"
        )
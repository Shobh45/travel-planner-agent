import requests
import os

from crewai.tools import BaseTool


class ForecastWeatherTool(BaseTool):
    name: str = "5-Day Weather Forecast Tool"

    description: str = (
        "Provides 5-day weather forecast data "
        "for a given city."
    )

    def _run(self, city: str) -> str:

        api_key = os.getenv("OPENWEATHER_API_KEY")

        url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={api_key}&units=metric"
        )

        response = requests.get(url)

        data = response.json()

        if response.status_code != 200:
            return f"Forecast data not found for {city}"

        forecasts = []

        for item in data["list"][:10]:

            date_time = item["dt_txt"]
            temp = item["main"]["temp"]
            weather = item["weather"][0]["description"]

            forecasts.append(
                f"{date_time}: {weather}, {temp}°C"
            )

        return "\n".join(forecasts)
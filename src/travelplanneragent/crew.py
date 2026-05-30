# Inserted Code
from crewai import LLM
import os
# Inserted Code


from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from crewai_tools import ScrapeWebsiteTool
from travelplanneragent.tools.weather_tool import WeatherTool
from travelplanneragent.tools.forecastweather_tool import ForecastWeatherTool
from travelplanneragent.tools.flightsearch_tool import FlightSearchTool
from travelplanneragent.tools.hotel_search_tool import HotelSearchTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Inserted Code
#gemini_llm = LLM(
#    model="gemini/gemini-2.5-flash",
#    api_key=os.getenv("GEMINI_API_KEY")
#)

openrouter_llm = LLM(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

search_tool = SerperDevTool()
weather_tool = WeatherTool()
scrape_website_tool = ScrapeWebsiteTool()
forecastweather_tool = ForecastWeatherTool()
flight_search_tool = FlightSearchTool()
hotel_search_tool = HotelSearchTool()
# Inserted Code

@CrewBase
class Travelplanneragent():
    """Travelplanneragent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            llm=openrouter_llm,
            tools=[search_tool, scrape_website_tool, weather_tool, forecastweather_tool],
            verbose=True
        )
    
    @agent
    def budget_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_analyst'], # type: ignore[index]
            llm=openrouter_llm,
            verbose=True
        )
    

    @agent
    def booking_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['booking_agent'], # type: ignore[index]
            llm=openrouter_llm,
            tools=[flight_search_tool, hotel_search_tool],
            verbose=True
        )


    @agent
#   def reporting_analyst(self) -> Agent:
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'], # type: ignore[index]
            llm=openrouter_llm,
            verbose=True
        )
    
    @agent
    def recommendation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['recommendation_agent'], # type: ignore[index]
            llm=openrouter_llm,
            tools=[search_tool, scrape_website_tool],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )
    
    @task
    def budget_task(self) -> Task:
        return Task(
            config=self.tasks_config['budget_task'], # type: ignore[index]
        )
    
    @task
    def booking_task(self) -> Task:
        return Task(
            config=self.tasks_config['booking_task'], # type: ignore[index]
        )

    @task
#   def reporting_task(self) -> Task:
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_task'], # type: ignore[index]
            output_file='report.md'
        )
    
    @task
    def recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['recommendation_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Travelplanneragent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

# test_agent.py
from dotenv import load_dotenv
load_dotenv()

from langchain_asi import ASI1ChatModel
from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool
from typing import List

from typing import Optional, Type
from langchain_asi import ASI1ChatModel
from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool
from typing import List

# Update the Calculator class with type annotations
class Calculator(BaseTool):
    name: str = "calculator"  # Add type annotation here
    description: str = "Useful for when you need to calculate mathematical expressions"
    
    def _run(self, query: str) -> str:
        try:
            return str(eval(query))
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")

# Do the same for WeatherTool
class WeatherTool(BaseTool):
    name: str = "weather"  # Add type annotation here
    description: str = "Get the weather for a specific location"
    
    def _run(self, location: str) -> str:
        # This is a mock implementation
        location = location.lower()
        if "london" in location:
            return "It's rainy and 15°C in London."
        elif "new york" in location or "nyc" in location:
            return "It's sunny and 22°C in New York."
        elif "tokyo" in location:
            return "It's cloudy and 20°C in Tokyo."
        else:
            return f"The weather in {location} is currently unavailable."
    
    def _arun(self, location: str):
        raise NotImplementedError("This tool does not support async")

# Create a list of tools
tools: List[BaseTool] = [Calculator(), WeatherTool()]

# Initialize the ASI1 model
llm = ASI1ChatModel(temperature=0)

# Use your utility function:
from langchain_asi.utils import create_asi_agent

# Create the agent with a different agent type
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Try this instead
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5  # Add this to prevent infinite loops
)

# Test the agent with different queries
test_queries = [
    "What is 25 * 63?",
    "What's the weather like in London?",
    "If it's 22°C in New York, what is that in Fahrenheit?"
]

for query in test_queries:
    print("\n" + "="*50)
    print(f"Query: {query}")
    print("="*50)
    try:
        response = agent.invoke(query)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")
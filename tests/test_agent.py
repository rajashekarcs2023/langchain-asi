# tests/test_agent.py
import os
import pytest
from langchain_asi import ASI1ChatModel
from langchain_asi.utils import create_asi_agent
from langchain.tools import BaseTool

# Skip tests if no API key is available
requires_api_key = pytest.mark.skipif(
    not os.environ.get("ASI1_API_KEY"),
    reason="ASI1_API_KEY environment variable not set"
)

class TestAgentIntegration:
    
    def setup_method(self):
        """Set up the test fixture."""
        self.model = ASI1ChatModel()
        
        # Define a simple calculator tool
        class Calculator(BaseTool):
            name: str = "calculator"
            description: str = "Useful for math calculations"
            
            def _run(self, query: str) -> str:
                try:
                    return str(eval(query))
                except Exception as e:
                    return f"Error: {str(e)}"
            
            def _arun(self, query: str):
                raise NotImplementedError("Async not supported")
        
        self.tools = [Calculator()]
    
    @requires_api_key
    def test_create_agent(self):
        """Test creating an agent with tools."""
        agent = create_asi_agent(
            tools=self.tools,
            system_prompt="You are a helpful assistant."
        )
        assert agent is not None
    
    @requires_api_key
    def test_agent_calculation(self):
        """Test that the agent can use tools to solve problems."""
        agent = create_asi_agent(
            tools=self.tools,
            system_prompt="You are a helpful assistant.",
            handle_parsing_errors=True
        )
        response = agent.invoke("What is 25 * 42?")
        
        # Check if '1050' is in the output field of the response
        assert "1050" in response['output']
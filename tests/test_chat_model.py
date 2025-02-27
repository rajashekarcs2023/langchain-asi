# tests/test_chat_model.py
import os
import pytest
from langchain_asi import ASI1ChatModel
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Skip tests if no API key is available
requires_api_key = pytest.mark.skipif(
    not os.environ.get("ASI1_API_KEY"),
    reason="ASI1_API_KEY environment variable not set"
)

class TestASI1ChatModel:
    
    def setup_method(self):
        """Set up the test fixture."""
        self.model = ASI1ChatModel()
    
    @requires_api_key
    def test_initialization(self):
        """Test model initialization with different parameters."""
        # Default initialization
        model1 = ASI1ChatModel()
        assert model1.model_name == "asi1-mini"
        assert model1.temperature == 0.7
        
        # Custom parameters
        model2 = ASI1ChatModel(model_name="custom-model", temperature=0.3)
        assert model2.model_name == "custom-model"
        assert model2.temperature == 0.3
    
    @requires_api_key
    def test_invoke_with_string(self):
        """Test model invocation with a string."""
        response = self.model.invoke("Hello, how are you?")
        assert isinstance(response, AIMessage)
        assert len(response.content) > 0
    
    @requires_api_key
    def test_invoke_with_messages(self):
        """Test model invocation with a list of messages."""
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="What is the capital of France?")
        ]
        response = self.model.invoke(messages)
        assert isinstance(response, AIMessage)
        assert len(response.content) > 0
        assert "Paris" in response.content
    
    @requires_api_key
    def test_bind_tools(self):
        """Test binding tools to the model."""
        from langchain.tools import tool
        
        @tool
        def calculator(expression: str) -> str:
            """Calculate a mathematical expression."""
            return str(eval(expression))
        
        tools = [calculator]
        model_with_tools = self.model.bind_tools(tools)
        assert model_with_tools is not None
from langchain.chat_models.base import BaseChatModel
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import requests
import os
from typing import List, Dict, Any, Optional, Union, Tuple

class ASI1ChatModel(BaseChatModel):
    """LangChain integration for ASI1 API chat models."""
    
    model_name: str = "asi1-mini"
    temperature: float = 0.7
    max_tokens: int = 4000
    api_key: Optional[str] = None
    api_base: str = "https://api.asi1.ai/v1"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get API key from environment or constructor
        self.api_key = kwargs.get("api_key", os.environ.get("ASI1_API_KEY"))
        if not self.api_key:
            raise ValueError("ASI1_API_KEY must be provided as an argument or environment variable")
        
        # Override default params if provided
        for param in ["model_name", "temperature", "max_tokens", "api_base"]:
            if param in kwargs:
                setattr(self, param, kwargs[param])
    
    def _generate(self, messages: List, stop: Optional[List[str]] = None, 
                 **kwargs) -> ChatResult:
        """Generate a completion using the ASI1 API."""
        
        # Convert LangChain message format to ASI1 format
        asi_messages = []
        for message in messages:
            if isinstance(message, SystemMessage):
                asi_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                asi_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                asi_messages.append({"role": "assistant", "content": message.content})
            elif hasattr(message, "content"):
                # If it's a string, treat it as a user message
                asi_messages.append({"role": "user", "content": str(message.content)})
            else:
                # If it's a string, treat it as a user message
                asi_messages.append({"role": "user", "content": str(message)})
        
        # Prepare the request payload
        payload = {
            "model": self.model_name,
            "messages": asi_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        # Add stop sequences if provided
        if stop:
            payload["stop"] = stop
        
        # Make the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=payload
        )
        
        # Parse the response
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Create an AIMessage
        message = AIMessage(content=content)
        
        # Create a ChatGeneration with the message
        generation = ChatGeneration(message=message)
        
        # Create and return a ChatResult
        chat_result = ChatResult(generations=[generation])
        
        # Add token usage if available
        if "usage" in result:
            chat_result.llm_output = {
                "token_usage": result["usage"],
                "model_name": self.model_name
            }
        
        return chat_result
    
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "asi1"
    
    def bind_tools(self, tools):
        """Bind tools to the model.
        
        Args:
            tools: List of tools to bind to the model
            
        Returns:
            A new instance of the model with the tools bound
        """
    # For models that don't natively support tool binding,
    # we just return the model itself
        return self
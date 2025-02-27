from langchain.agents import initialize_agent, AgentType
from langchain.tools.base import BaseTool
from typing import List, Optional
from langchain_asi.chat_models import ASI1ChatModel

def create_asi_agent(tools: List[BaseTool], 
                    system_prompt: Optional[str] = None,
                    model_name: str = "asi1-mini",
                    temperature: float = 0.7,
                    max_tokens: int = 4000,
                    api_key: Optional[str] = None,
                    api_base: Optional[str] = None,
                    agent_type: AgentType = AgentType.OPENAI_FUNCTIONS,
                    handle_parsing_errors: bool = True):
    """Create a LangChain agent using ASI1."""
    
    # Create ASI1 model
    llm_kwargs = {
        "model_name": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    if api_key:
        llm_kwargs["api_key"] = api_key
    if api_base:
        llm_kwargs["api_base"] = api_base
        
    llm = ASI1ChatModel(**llm_kwargs)
    
    # Create and return agent
    if system_prompt:
        agent_kwargs = {"system_message": system_prompt}
    else:
        agent_kwargs = {}
        
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=agent_type,
        agent_kwargs=agent_kwargs,
        verbose=True,
        handle_parsing_errors=handle_parsing_errors
    )
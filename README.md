# langchain-asi
# LangChain ASI1 Integration

A lightweight, easy-to-use integration package that connects ASI1's API with the LangChain ecosystem.

## Overview

This package provides seamless integration between ASI1's API and LangChain, allowing you to use ASI1's language models with LangChain's frameworks, agents, and tools. The integration is designed to be a drop-in replacement for other LLM providers like OpenAI and Anthropic, taking advantage of ASI1's OpenAI-compatible API.

## Features

- **Simple Integration**: Easily swap ASI1 models into your existing LangChain applications
- **Conversation Support**: Full support for multi-turn conversations with memory
- **System Instructions**: Control model behavior with system messages
- **Agent Support**: Create LangChain agents powered by ASI1 models
- **Tool Integration**: Connect ASI1 models with LangChain tools and utilities
- **Parameter Control**: Customize temperature, max tokens, and other model parameters
- **Error Handling**: Robust error handling for API communication

## Installation

```bash
# From source
git clone https://github.com/yourusername/langchain-asi.git
cd langchain-asi
pip install -e .

# Or when published on PyPI
pip install langchain-asi
```
## Quick Start

### Basic Usage

```python
from langchain_asi import ASI1ChatModel
from dotenv import load_dotenv

# Load API key from .env file (recommended)
load_dotenv()

# Initialize the model
llm = ASI1ChatModel()

# Simple query
response = llm.invoke("What are the three laws of robotics?")
print(response.content)
```

### Conversation with System Message

```python
from langchain_asi import ASI1ChatModel
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Initialize with custom parameters
llm = ASI1ChatModel(
    model_name="asi1-mini",
    temperature=0.3,
    max_tokens=2000
)

# Create a conversation with a system message
messages = [
    SystemMessage(content="You are a helpful assistant that always responds in rhymes."),
    HumanMessage(content="Tell me about artificial intelligence.")
]

response = llm.invoke(messages)
print(response.content)

# Continue the conversation
messages.append(response)
messages.append(HumanMessage(content="What are its potential risks?"))
response = llm.invoke(messages)
print(response.content)
```
## Working with LangChain Chains

```python
from langchain_asi import ASI1ChatModel
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize the model
llm = ASI1ChatModel()

# Create a simple prompt template
template = "Write a short {style} poem about {topic}."
prompt = PromptTemplate(template=template, input_variables=["style", "topic"])

# Create a chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain
result = chain.run(style="haiku", topic="artificial intelligence")
print(result)
```

## Creating Agents

### Simple Agent with Tools

```python
from langchain_asi import ASI1ChatModel, create_asi_agent
from langchain.tools import BaseTool
from typing import List

# Define a calculator tool
class Calculator(BaseTool):
    name: str = "calculator"
    description: str = "Useful for performing mathematical calculations"
    
    def _run(self, query: str) -> str:
        try:
            return str(eval(query))
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")

# Create a list of tools
tools = [Calculator()]

# Create an agent using the utility function
agent = create_asi_agent(
    tools=tools,
    system_prompt="You are a helpful assistant that's good at math.",
    temperature=0.2
)

# Use the agent
result = agent.run("If I have 25 apples and give 7 to my friend, then eat 3 myself, how many do I have left?")
print(result)
```

## API Configuration

### Environment Variables

The recommended way to set your ASI1 API key is via environment variables:

```bash
export ASI1_API_KEY=your_api_key_here
```

Or in your Python code:

```python
import os
os.environ["ASI1_API_KEY"] = "your_api_key_here"
```

### Using .env Files

For development, you can store your API key in a `.env` file:

```
ASI1_API_KEY=your_api_key_here
```

Then load it with:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Direct Parameter

You can also pass the API key directly when initializing the model:

```python
llm = ASI1ChatModel(api_key="your_api_key_here")
```

## Advanced Configuration

### Custom API Base URL

If you need to use a different API endpoint:

```python
llm = ASI1ChatModel(
    api_base="https://your-custom-endpoint.com/v1"
)
```

### Model Parameters

Configure various model parameters:

```python
llm = ASI1ChatModel(
    model_name="asi1-mini",  # Model name
    temperature=0.7,         # Randomness (0-1)
    max_tokens=8000          # Maximum response length
)
```

## Integration with LangGraph

For more complex agent workflows, you can integrate ASI1 models with LangGraph:

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_asi import ASI1ChatModel
from langchain_core.tools import tool

# Define a tool
@tool
def search(query: str):
    """Search for information."""
    if "weather" in query.lower():
        return "It's currently sunny and 22°C."
    return "No specific information found."

# Initialize the ASI1 model
model = ASI1ChatModel(temperature=0)

# Initialize memory
checkpointer = MemorySaver()

# Create a LangGraph agent
app = create_react_agent(model, [search], checkpointer=checkpointer)

# Use the agent
result = app.invoke(
    {"messages": [{"role": "user", "content": "What's the weather today?"}]},
    config={"configurable": {"thread_id": "unique-thread-id"}}
)

# Get the final response
print(result["messages"][-1].content)
```

## Limitations

- The current implementation does not support native function calling (available in some other LLMs)
- Streaming responses are not yet implemented
- Some advanced LangChain features may require additional configuration

## Troubleshooting

### API Key Issues

If you encounter authentication errors, check that your API key is:
- Correctly set in your environment or passed to the model
- Valid and active in your ASI1 account

### Agent Parsing Errors

When using agents, you may see parsing errors. These can often be resolved by:
- Setting `handle_parsing_errors=True` when creating the agent
- Using the `ZERO_SHOT_REACT_DESCRIPTION` agent type which is more forgiving

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
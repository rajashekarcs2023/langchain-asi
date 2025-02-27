# test_langgraph.py
from dotenv import load_dotenv
load_dotenv()

import os
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_asi import ASI1ChatModel

# Define a simple search tool
@tool
def search(query: str):
    """Call to search for information."""
    # This is a mock implementation
    if "weather" in query.lower():
        return "It's currently sunny and 22°C."
    elif "population" in query.lower():
        return "The population is approximately 8.8 million people."
    elif "capital" in query.lower():
        return "The capital of France is Paris."
    else:
        return "No specific information found for this query."

# Define a simple calculator tool
@tool
def calculator(expression: str):
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error in calculation: {str(e)}"

# List of tools
tools = [search, calculator]

# Initialize the ASI1 model
model = ASI1ChatModel(
    model_name="asi1-mini",
    temperature=0,  # Lower temperature for more deterministic responses
    max_tokens=4000
)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Create the agent
print("Creating LangGraph ReAct agent with ASI1...")
app = create_react_agent(model, tools, checkpointer=checkpointer)

# Test queries
test_queries = [
    "What is the capital of France?",
    "What is 42 * 18?",
    "What's the weather like today?"
]

# Run the tests
for i, query in enumerate(test_queries):
    print(f"\n{'='*50}")
    print(f"Test {i+1}: {query}")
    print(f"{'='*50}")
    
    try:
        # Create a unique thread ID for each conversation
        thread_id = f"test-thread-{i}"
        
        # Invoke the agent
        final_state = app.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config={"configurable": {"thread_id": thread_id}}
        )
        
        # Print the final response
        print("\nFinal Response:")
        print(final_state["messages"][-1].content)
        
    except Exception as e:
        print(f"Error: {str(e)}")
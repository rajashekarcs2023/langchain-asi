#In place of anthropic, ASI model can be used
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_asi import ASI1ChatModel  # Your custom ASI1 integration
from langchain_core.tools import tool

# Define the tools for the agent to use
@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder implementation
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

# Create the list of tools
tools = [search]

# Initialize the ASI1 model
model = ASI1ChatModel(model_name="asi1-mini", temperature=0)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Create the ReAct agent
app = create_react_agent(model, tools, checkpointer=checkpointer)

# Use the agent to answer a weather question
final_state = app.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config={"configurable": {"thread_id": 42}}
)

# Print the final response
print(final_state["messages"][-1].content)
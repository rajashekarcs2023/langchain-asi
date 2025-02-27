# test_examples.py
from dotenv import load_dotenv
load_dotenv()

from langchain_asi import ASI1ChatModel
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Initialize the model
llm = ASI1ChatModel()

print("="*50)
print("Example 1: Basic Chat Completion")
print("="*50)
response = llm.invoke("Explain what quantum computing is in one sentence.")
print(f"Response: {response.content}")

print("\n"+"="*50)
print("Example 2: Using System Messages")
print("="*50)
messages = [
    SystemMessage(content="You are a helpful assistant that always responds in rhymes."),
    HumanMessage(content="Tell me about artificial intelligence.")
]
response = llm.invoke(messages)
print(f"Response: {response.content}")

print("\n"+"="*50)
print("Example 3: Multi-turn Conversation")
print("="*50)
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My name is Alex."),
    AIMessage(content="Hello Alex! It's nice to meet you. How can I help you today?"),
    HumanMessage(content="What's my name?")
]
response = llm.invoke(messages)
print(f"Response: {response.content}")
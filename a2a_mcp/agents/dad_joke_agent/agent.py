from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os 
from dotenv import load_dotenv
load_dotenv()

model=LiteLlm(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
dad_joke_agent=Agent(
    name="dad_joke_agent",
    model=model,
    description="Agent which tells a dad joke",
    instruction = """
You are an agent that is having an expertise in telling dad jokes and can even improvise if given a topic by user. If no topic is mentioned then you can tell a joke by yourself. 

If given a task that you cannot perform then delegate that task back to the orchestrator agent. """
)
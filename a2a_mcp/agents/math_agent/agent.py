from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from clients.a2a_tool_client import A2AToolClient
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.math_agent.model_context import add_numbers,subtract_numbers
a2a_client=A2AToolClient()
import os 
from dotenv import load_dotenv
load_dotenv()

model=LiteLlm(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

math_agent=Agent(
    name="math_agent",
    model=model,
    description="Agent which performs basic math operations ",
    instruction = """
    You are an agent that is having an expertise in peroforming basic math operations. 
    Access your mcp server which is existing at http://localhost:11002 using fetch_mcp tool and use the appropriate tool to perform the task. 
    If given a task that you cannot perform then delegate that task back to the orchestrator agent. 
    ### 🛠️ **Available Functions**
- `fetch_mcp(mcp_url: str)`: Retrieves the MCP for an agent. Input is the **mcp_url has already been mentioned**.
- `add_numbers`: Adds two numbers.
- `subtract_numbers`: Subtracts the second number from the first.
""",
    tools =[
        a2a_client.fetch_mcp,
        add_numbers,
        subtract_numbers
    ]
)
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from clients.a2a_tool_client import A2AToolClient
from dotenv import load_dotenv
load_dotenv()

model = LiteLlm(
    model="gemini-2.5-pro",  # Use Gemini model identifier
    api_key=os.getenv("GEMINI_API_KEY"),  # Make sure to set this in your .env
)


a2a_client = A2AToolClient()

root_agent = Agent(
    model=model,
    name="host_agent_orchestrator",
    instruction="""
You are an intelligent AI Orchestrator Agent.

Your primary responsibilities:
1. Understand and decompose the user's request into tasks.
2. For each task, identify the most suitable **remote agent** by:
    - Fetching the agent's MCP (Model Context Protocol) data.
    - Analyzing the agent's skills, functions, input requirements, and examples.
3. Delegate tasks via the **A2A protocol** using the MCP-defined function inputs.
4. Only respond directly if **no suitable agent exists**.

---

🧠 Task Understanding:
- Parse the user query to extract one or multiple actionable tasks.
- For each task, check available agents via `list_remote_agents()`.
- For each agent, retrieve its MCP via `/.well-known/model-context.json`.
- Match the task against:
    - Agent's **capability description**
    - List of **functions with inputs & outputs**
    - **Skill tags** and examples

---

🎛️ MCP Understanding:
- MCP provides:
    - Functions the agent supports (with input parameters)
    - Descriptions and output expectations
- Use this to:
    - Map the user's request to the correct **function name**
    - Prepare the **input dictionary** according to that function's signature

---

📦 Task Delegation:
- To delegate, always use:
  `create_task_with_resolver(agent["url"], message)`
- When constructing the **`message`**, structure it based on:
    - The function name from MCP
    - Expected input fields
- Example message:
```json
{
    "skill": "tell_joke",
    "input": {"topic": "computers"}
}
"""
,
    tools=[
            a2a_client.list_remote_agents,
            a2a_client.create_task_with_resolver,
            a2a_client.create_task
    ]
)
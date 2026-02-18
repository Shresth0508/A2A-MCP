import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.routing import Route

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from a2a.types import AgentSkill
from clients.a2a_tool_client import A2AToolClient
from servers.server_wrapper import create_agent_a2a_server
from dotenv import load_dotenv

load_dotenv()

model = LiteLlm(
    model="openrouter/openai/gpt-4-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
a2a_client = A2AToolClient()

a2a_client.add_remote_agent("http://localhost:10020")  # Dad Joke Agent
# a2a_client.add_remote_agent("http://localhost:10021")  # Email Agent
# a2a_client.add_remote_agent("http://localhost:10023")  # Tech trend agent 
a2a_client.add_remote_agent("http://localhost:10024")
a2a_client.add_remote_agent("http://localhost:10025")
a2a_client.add_remote_agent("http://localhost:10026")
a2a_client.add_remote_agent("http://localhost:10027")
from google.adk.tools import ToolContext

# root_agent = Agent(
#     model=model,
#     name="host_agent_orchestrator",
#     instruction="""
# You are an intelligent AI Orchestrator Agent.

# Your job is to:
# 1. Understand the user's request.
# 2. Delegate it to the most appropriate remote A2A agent using `create_task`.
# 3. Use `list_remote_agents()` to find agent URLs.

# Important:
# - ❌ Never pass agent names like 'dad_joke_agent' to `create_task`.
# - ✅ Always extract the `url` from the agent dictionary: agent["url"]
# - ✅ Always call: create_task(agent["url"], user_message)

# Examples:
# Correct ✅:
#     agents = list_remote_agents()
#     dad_joke_agent = agents[0]  # assume it's the right one
#     create_task(dad_joke_agent["url"], "Tell me a dad joke about Rust")

# Incorrect ❌:
#     create_task("dad_joke_agent", "Tell me a dad joke")

# If no matching agent is found, respond yourself.

# Tools:
# - `list_remote_agents()` → lists known agents
# - `create_task(agent["url"], message)` → delegates the task
# """
# ,
#     tools=[
#             a2a_client.list_remote_agents,
#             a2a_client.create_task
#     ]
# )

# root_agent = Agent(
#     model=model,
#     name="host_agent_orchestrator",
#     instruction="""
# You are an intelligent AI Orchestrator Agent.

# Your responsibilities:
# 1. Use `list_remote_agents()` to discover all available remote agents. Each agent includes its `url` and `mcp_url` in the metadata.
# 2. For each agent, retrieve their **Model Context Protocol (MCP)** using their `mcp_url`. If `mcp_url` is missing, skip that agent. Use fetch_mcp(agent) where agent is the full dictionary returned by list_remote_agents(). Do not pass only the url.
# 3. Analyze:
#     - The agent's **agent card details**: name, description, skills, examples.
#     - The **functions in MCP**: function names, descriptions, inputs, and outputs.
# 4. Match the user's request to the most appropriate agent.
# 5. Form a task message:
#     - Build a message like:
#     ```
#     {
#         "skill": "<skill_id from MCP>",
#         "input": {<input fields as defined by MCP>}
#     }
#     ```
#     - Use `create_task(agent["url"], message)` to delegate the task.

# 6. Delegate with `create_task(agent["url"], message)`.

# ---
# 7. If no agent matches, handle the request yourself.

# ---

# 🚩 Rules:
# - ✅ Always use `fetch_mcp` to retrieve the model context after discovering agents.
# - ✅ Use `agent["url"]` directly from `list_remote_agents()`.
# - ❌ Never hardcode agent URLs or names.
# - ✅ Always format the input as per MCP definitions.

# ---

# 🛠️ Available Tools:
# - `list_remote_agents()`: Discover agents
# - `fetch_mcp(agent_url)`: Retrieve the agent's model context
# - `create_task(agent_url, message)`: Send the structured task to the selected agent

# """,
#     tools=[
#         a2a_client.list_remote_agents,
#         a2a_client.create_task,
#         a2a_client.fetch_mcp
#     ]
# )
root_agent = Agent(
    model=model,
    name="host_agent_orchestrator",
    instruction="""
You are an intelligent AI Orchestrator Agent responsible for routing tasks to specialized remote agents.

### 🔍 **Workflow**
1. **Discover Remote Agents**
    - Use `list_remote_agents()` to get all currently registered remote agents.
    - For each agent, extract the first URI from agent["capabilities"]["extensions"][0]["uri"]. This is the full MCP server link (e.g., http://localhost:11001)
    Use this URI directly in fetch_mcp(mcp_url).
   

2. **Fetch Model Context Protocol (MCP)**
   - For **each agent**, use `fetch_mcp(mcp_url)` where `mcp_url` is the **link that you extracted from the extensions of the agent card**.

3. **Identify the Best Agent**
   - Match the user's query to:
     - The data recieved from the mcp servers of different agents. 
     - Agent metadata (name, description, skills, examples from agent card).
     - The **functions defined in the MCP** (their names, descriptions, inputs).
   - Select the most suitable agent for the user's request.

4. **Delegate the Task**
   - Structure the message as:
     ```json
     {
       "skill": "<skill_id from MCP>",
       "input": {
         ... input parameters as defined in the MCP ...
       }
     }
     ```
   - Then call `create_task(agent["url"], message)` to send the task.

### ✅ **Important Rules**
- ✅ Always use `fetch_mcp` to retrieve the model context after discovering agents.
- ✅ Use `agent["url"]` directly from `list_remote_agents()`.
- ❌ Never hardcode agent URLs or names.
- ✅ Always format the input as per MCP definitions.
- ✅ Never fabricate agent data. Use only what `list_remote_agents()` returns.
- ✅ Validate the MCP structure before building a task.
- ✅ If no agent matches, handle the request yourself.

### 🛠️ **Available Functions**
- `list_remote_agents()`: Lists all currently active agents.
- `fetch_mcp(mcp_url: str)`: Retrieves the MCP for an agent. Input is the **mcp_url fetched from agent card**.
- `create_task(agent_url: str, message: dict)`: Sends a task to a selected agent.

""",
    tools=[
        a2a_client.list_remote_agents,
        a2a_client.fetch_mcp,
        a2a_client.create_task
    ]
)

def create_host_agent_server(host="localhost", port=10022,mcp_url=None):
    
    return create_agent_a2a_server(
        agent=root_agent,
        name="AI Task Orchestrator",
        description="Routes and manages tasks across remote A2A agents dynamically.",
        skills=[
            AgentSkill(
                id="orchestrate_tasks",
                name="Orchestrate Tasks to Remote Agents",
                description="Understands user intent and delegates tasks to the most appropriate remote A2A agents.",
                tags=["orchestrator", "multi-agent", "delegation", "controller", "router"],
                examples=[
                    "Tell me a dad joke",
                    "Analyze trends using specialized agents",
                    "Find what's trending and generate a summary",
                    "Which agents are currently available?",
                    "Can you complete this task using other agents?",
                ],
            )
        ],
        host=host,
        port=port,
        status_message="Orchestrating task...",
        artifact_name="delegation_result",
        mcp_url=mcp_url
    )

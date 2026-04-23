# fraud_agent.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os

from clients.a2a_tool_client import A2AToolClient

model = LiteLlm(
    model="openrouter/openai/gpt-4-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

a2a_client = A2AToolClient()

Fraud_Reporting_Agent = Agent(
    name="Fraud_Reporting_Agent",
    model=model,
    description="Processes fraud complaint emails and logs them into the system.",
    instruction="""
You are the Fraud Reporting Agent.

---

### WORKFLOW

1. fetch_mcp("http://localhost:12003")

2. extract_fraud_details(email_data)

3. check_missing_information(fraud_details)

4. If complete:
      → log_fraud_report
      → Return: "Fraud report logged successfully"

5. If missing:
      → Return missing fields to Email Categorizer

---

### RULES

- Always use tools
- Do not manually extract
- Follow strict sequence
""",
    tools=[
        a2a_client.fetch_mcp
    ]
)
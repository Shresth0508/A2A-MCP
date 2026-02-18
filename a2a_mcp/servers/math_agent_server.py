import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.routing import Route

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.math_agent.agent import math_agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


def create_math_agent_server(host="localhost", port=10024, mcp_url=None):
    return create_agent_a2a_server(
        agent=math_agent,
        name="Math Agent",
        description="Performs simple maths calculations like addition and subtraction.",
        skills=[
            AgentSkill(
                id="add_numbers",
                name="Add Numbers",
                description="Adds two numbers together.",
                tags=["math", "addition", "sum", "numbers"],
                examples=[
                    "What is 5 + 7?",
                    "Add 12 and 20",
                    "Give me the sum of 3.5 and 4.2"
                ],
            ),
            AgentSkill(
                id="subtract_numbers",
                name="Subtract Numbers",
                description="Subtracts the second number from the first.",
                tags=["math", "subtraction", "difference", "numbers"],
                examples=[
                    "What is 10 minus 4?",
                    "Subtract 5 from 15",
                    "What's the difference between 9 and 3?"
                ],
            )
        ],
        host=host,
        port=port,
        status_message="Math Agent ready to calculate!",
        artifact_name="math_tools",
        mcp_url=mcp_url
    )

if __name__ == "__main__":
    server = create_math_agent_server()
    uvicorn.run(server, host="localhost", port=10024)


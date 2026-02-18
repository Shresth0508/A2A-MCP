import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agents.Email_categorizer_agent.agent import Email_Categorizer_Agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


def create_email_categorizer_agent_server(host="localhost", port=10026, mcp_url=None):
    return create_agent_a2a_server(
        agent=Email_Categorizer_Agent,
        name="Email Categorizer Agent",
        description="Categorizes structured emails into predefined banking categories.",
        skills=[
            AgentSkill(
                id="categorize_email",
                name="Categorize Email",
                description="Categorizes a structured email JSON into one of the four banking categories.",
                tags=["email", "categorization", "banking", "classification"],
                examples=[
                    "Classify an email requesting a credit card limit increase.",
                    "Categorize an email about loan approval.",
                    "Identify a fraud dispute email.",
                    "Classify an email applying for a credit card."
                ]
            )
        ],
        host=host,
        port=port,
        status_message="Email Categorizer Agent is ready to classify emails!",
        artifact_name="email_categorizer_agent",
        mcp_url=mcp_url
    )


# if __name__ == "__main__":
#     app = create_email_categorizer_agent_server()
#     uvicorn.run(app, host="localhost", port=10023)

import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.routing import Route

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.Email_Reciever_Agent.agent import Email_Reciever_Agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


def create_email_receiver_agent_server(host="localhost", port=10025, mcp_url=None):
    return create_agent_a2a_server(
        agent=Email_Reciever_Agent,
        name="Email Receiver Agent",
        description="Accepts and parses raw email input into structured data using the MCP-provided parse_email tool.",
        skills=[
            AgentSkill(
                id="parse_email",
                name="Parse Email",
                description="Parses raw email text into structured data including sender, subject, body, and attachments.",
                tags=["email", "parsing", "structure", "attachments", "subject"],
                examples=[
                    "Parse this email: From: john@example.com Subject: Credit Card Request Body: I want a credit card. Attachments: ID_Proof.pdf",
                    "Extract sender, subject, and body from an email.",
                    "Get attachments mentioned in the email text."
                ]
            )
        ],
        host=host,
        port=port,
        status_message="Email Receiver Agent is ready to parse emails!",
        artifact_name="email_tools",
        mcp_url=mcp_url
    )


# if __name__ == "__main__":
#     server = create_email_receiver_agent_server()
#     uvicorn.run(server, host="localhost", port=10025)

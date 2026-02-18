import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.credit_application_agent.agent import Credit_Application_Agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


def create_credit_application_agent_server(host="localhost", port=12000, mcp_url=None):
    return create_agent_a2a_server(
        agent=Credit_Application_Agent,
        name="Credit Application Agent",
        description="Processes credit card applications and stores applicant information.",
        skills=[
            AgentSkill(
                id="process_credit_application",
                name="Process Credit Card Application",
                description="Takes user application details and processes/validates the credit card application.",
                tags=["credit card", "application", "banking", "process application", "credit limit"],
                examples=[
                    "Process this credit card application",
                    "Handle applicant data for credit card issuance",
                    "Register new credit card applicant"
                ],
            )
        ],
        host=host,
        port=port,
        status_message="Credit Application Agent is up and running...",
        artifact_name="credit_application",
        mcp_url=mcp_url
    )
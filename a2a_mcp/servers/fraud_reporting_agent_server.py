import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.fraud_agent.agent import Fraud_Reporting_Agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


def create_fraud_reporting_agent_server(host="localhost", port=12003, mcp_url=None):
    return create_agent_a2a_server(
        agent=Fraud_Reporting_Agent,
        name="Fraud Reporting Agent",
        description="Processes fraud complaint emails and logs them into the database.",
        skills=[
            AgentSkill(
                id="process_fraud_report",
                name="Process Fraud Report",
                description="Extracts fraud complaint details from user input and logs them into the system.",
                tags=[
                    "fraud",
                    "fraud report",
                    "banking",
                    "unauthorized transaction",
                    "complaint",
                    "customer issue"
                ],
                examples=[
                    "Report an unauthorized transaction",
                    "Log a fraud complaint from this email",
                    "Customer reporting suspicious transaction",
                    "Register a fraud incident"
                ],
            )
        ],
        host=host,
        port=port,
        status_message="Fraud Reporting Agent is up and running...",
        artifact_name="fraud_report",
        mcp_url=mcp_url
    )
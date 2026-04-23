import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.faq_agent.agent import FAQ_Agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


def create_faq_agent_server(host="localhost", port=12004, mcp_url=None):
    return create_agent_a2a_server(
        agent=FAQ_Agent,
        name="FAQ Agent",
        description="Handles general banking queries using a hybrid FAQ system (rule-based + LLM fallback).",
        skills=[
            AgentSkill(
                id="answer_faq",
                name="Answer FAQ",
                description="Answers general banking-related questions from users.",
                tags=[
                    "faq",
                    "banking",
                    "questions",
                    "help",
                    "support",
                    "information"
                ],
                examples=[
                    "How do I apply for a credit card?",
                    "What is the minimum salary required for a credit card?",
                    "How can I report fraud?",
                    "What is a credit limit?",
                    "How long does approval take?"
                ],
            )
        ],
        host=host,
        port=port,
        status_message="FAQ Agent is up and running...",
        artifact_name="faq_response",
        mcp_url=mcp_url
    )
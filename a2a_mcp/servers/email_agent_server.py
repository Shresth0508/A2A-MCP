import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.routing import Route

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.email_writer_agent.agent import email_agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill



def create_email_agent_server(host="localhost", port=10021):
    return create_agent_a2a_server(
        agent=email_agent,
        name="Email Agent",
        description="Writes both formal and informal emails based on user requests",
        skills=[
            AgentSkill(
                id="write_email",
                name="Write an Email",
                description="Composes a formal or informal email based on the user's input and tone preference.",
                tags=[
                    "email", "write email", "compose email", "formal email", 
                    "informal email", "message writing", "communication", 
                    "business email", "friendly email"
                ],
                examples=[
                    "Write a formal email to my professor requesting an extension",
                    "Draft an informal email to a friend about my vacation",
                    "Send a professional follow-up email after an interview"
                ],
            )
        ],
        host=host,
        port=port,
        status_message="Getting ready to write your perfect email...",
        artifact_name="email_writer"
    )




main_app = FastAPI()

@main_app.get("/")
def health():
    return {"message": "Email Writer Agent server is healthy!"}


main_app.mount("/a2a", create_email_agent_server())


if __name__ == "__main__":
    uvicorn.run("servers.email_agent_server:main_app", host="localhost", port=10020, reload=True)

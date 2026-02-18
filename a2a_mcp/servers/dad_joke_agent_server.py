import uvicorn
import sys
import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.routing import Route

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.dad_joke_agent.agent import dad_joke_agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill


# # ✅ This function is used by main.py to start the server
# def create_dad_joke_agent_server(host="localhost", port=10020):
#     return create_agent_a2a_server(
#         agent=dad_joke_agent,
#         name="Dad Joke Agent",
#         description="Tells hilarious (and terrible) dad jokes, optionally on a topic.",
#         skills=[
#             AgentSkill(
#                 id="tell_joke",
#                 name="Tell a Dad Joke",
#                 description="Generates a dad joke. Can take a topic or be spontaneous.",
#                 tags=["jokes", "humor", "dad jokes", "funny", "comedy", "laugh", "entertainment", "tell joke", "make me laugh"],
#                 examples=[
#                     "Tell me a dad joke",
#                     "Give me a joke about computers",
#                     "Make me laugh"
#                 ],
#             )
#         ],
#         host=host,
#         port=port,
#         status_message="Getting ready to make you laugh...",
#         artifact_name="dad_joke"
#     )


# # ✅ Optional: FastAPI app wrapper with health check
# main_app = FastAPI()

# # Mount the A2A app under /a2a
# @main_app.get("/")
# def health():
#     return {"message": "Dad Joke Agent server is healthy!"}
# #
# @main_app.get("/.well-known/model-context.json")
# def serve_model_context():
#     print("Dad_joke_agent mcp server visited")
#     return JSONResponse(content=model_context)

# main_app.mount("/a2a", create_dad_joke_agent_server())


# # ✅ Optional standalone run for manual testing
# if __name__ == "__main__":
#     uvicorn.run("servers.dad_joke_agent_server:main_app", host="localhost", port=10020)

def create_dad_joke_agent_server(host="localhost", port=10020,mcp_url=None):
    return create_agent_a2a_server(
        agent=dad_joke_agent,
        name="Dad Joke Agent",
        description="Tells dad jokes optionally on a topic.",
        skills=[
            AgentSkill(
                id="tell_joke",
                name="Tell a Dad Joke",
                description="Generates a dad joke. Can take a topic or be spontaneous.",
                tags=["jokes", "humor", "dad jokes", "funny", "comedy", "laugh", "entertainment", "tell joke", "make me laugh"],
                examples=[
                    "Tell me a dad joke",
                    "Give me a joke about computers",
                    "Make me laugh"
                ],
            )
        ],
        host=host,
        port=port,
        status_message="Getting ready to make you laugh...",
        artifact_name="dad_joke",
        mcp_url=mcp_url
    )

# main_app=create_dad_joke_agent_server()
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("servers.dad_joke_agent_server:main_app", host="localhost", port=10020, reload=True)
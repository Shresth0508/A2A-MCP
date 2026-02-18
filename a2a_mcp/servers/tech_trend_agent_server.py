import uvicorn
import sys
import os

from fastapi import FastAPI

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.tech_trends_agent.agent import tech_trend_agent
from servers.server_wrapper import create_agent_a2a_server
from a2a.types import AgentSkill

def create_tech_trend_agent_server(host="localhost", port=10023):
    return create_agent_a2a_server(
        agent=tech_trend_agent,
        name="Tech Trends Agent",
        description="Fetches and summarizes recent technology trends from domains like AI, web3, and software development.",
        skills=[
            AgentSkill(
                id="search_trending_tech",
                name="Search Tech Trends",
                description="Searches for recent developments and trends in a specific technology domain (e.g., AI, Web3, cloud computing).",
                tags=["technology", "trends", "search", "tech news", "AI", "blockchain", "software", "web3"],
                examples=[
                    "What's trending in AI?",
                    "Show me recent developments in blockchain",
                    "Give me the latest tech tools in web development"
                ]
            )
        ],
        host=host,
        port=port,
        status_message="Searching the web for recent technology trends...",
        artifact_name="tech_trends_agent"
    )
main_app = FastAPI()

@main_app.get("/")
def health():
    return {"message": "Tech Trends Agent server is healthy!"}


main_app.mount("/a2a", create_tech_trend_agent_server())

if __name__ == "__main__":
    uvicorn.run("servers.tech_trend_agent_server:main_app", host="localhost", port=10023, reload=True)

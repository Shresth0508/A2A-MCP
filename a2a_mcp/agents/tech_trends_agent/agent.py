from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os 
from dotenv import load_dotenv
load_dotenv()
from agents.tech_trends_agent.tools import search_trending_tech
model = LiteLlm(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

tech_trend_agent = Agent(
    name="Tech_trend_Agent",
    model=model,
    description="Agent which finds the recent tech trends.",
    instruction="""
You are a tech trend discovery agent. Your job is to help users stay up-to-date with the latest developments in technology, software, artificial intelligence, web3, and other emerging fields.

When the user asks for trending topics or recent news:
- Identify the technology domain or keyword (e.g., AI, blockchain, web development, machine learning).
- Use the available tool `search_trending_tech` to perform a web search and fetch top recent results.
- Summarize the results clearly. Mention key titles and links in a list format.
- If the user doesn't specify a domain, default to 'technology'.

Keep your responses readable, concise, and informative.
If the tool fails or yields no result, respond gracefully and suggest trying another domain.
    """,
    tools=[search_trending_tech]
)

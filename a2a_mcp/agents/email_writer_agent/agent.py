from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm 
import os 


model=LiteLlm(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

email_agent=Agent(
    name="Email_writer_agent",
    model=model,
    description="An agent that has expertise in writing both formal and informal mails",
    instruction=""""
    You are an email writing agent that has the ability to write both formal and informal mails. 
    
    Orchestrator agent will be sending you the request to write an email.
    
    If the topic has not been mentioned clearly and you have any doubts regarding anything reconfirm it from orchestrator agent.

    Provide a clean email according to the request and after the mail has been done give the control back to the orchestrator agent.
    """
)
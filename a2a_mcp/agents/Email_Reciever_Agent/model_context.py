from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
from litellm import completion
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.models.lite_llm import LiteLlm

app = FastAPI()

# Initialize LLM model
model = LiteLlm(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


model_context = {
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Parses raw email text and returns structured data such as sender, subject, body, and attachments."
        },
        {
            "name": "functions",
            "type": "function",
            "content": [
                {
                    "name": "parse_email",
                    "description": "Parses raw email text into structured components.",
                    "inputs": ["raw_email"],
                    "output": "structured_email_json"
                }
            ]
        }
    ]
}

import json
import asyncio

async def parse_email(raw_email: str) -> dict:
    """
    Parses a raw email string into structured JSON using the LLM.
    """
    prompt = f"""
You will receive a raw email text. Your task is to extract and return the following structured JSON:
- sender: <email sender>
- subject: <email subject>
- body: <main body of the email>
- attachments: <list of attachment file names, if mentioned, else an empty list>

### Raw Email:
{raw_email}

### Output JSON format:
{{
    "sender": "...",
    "subject": "...",
    "body": "...",
    "attachments": ["...", "..."]
}}

Strictly output only the JSON block — no explanations, no text before or after. Return only valid JSON.
"""
    print("Using parse_email tool from MCP")

    full_response = ""
    try:
        response = completion(messages=[{"role": "user", "content": prompt}],
                                model="openrouter/openai/gpt-4-turbo",
                                api_key=os.getenv("OPENROUTER_API_KEY"))
        content = response['choices'][0]['message']['content']
        print("Extracting application details using LLM...")
        return json.loads(content)
    except Exception as e:
        print("Error during LLM parsing:", e)
        return {"error": str(e)}


@app.get("/.well-known/model-context.json")
def get_model_context():
    return JSONResponse(content=model_context)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=12000)

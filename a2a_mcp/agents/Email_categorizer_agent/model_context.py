from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.adk.models.lite_llm import LiteLlm

app = FastAPI()

# Initialize LLM model
model = LiteLlm(
    model="openrouter/openai/gpt-4-turbo",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

model_context = {
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Categorizes structured emails and delegates tasks to appropriate banking agents."
        },
        {
            "name": "categories",
            "type": "list",
            "content": [
                "Credit Card Application",
                "Loan Approval Request",
                "Fraud / Dispute / Customer Support",
                "Credit Card Limit Extension / Due Date Change"
            ]
        },
        {
            "name": "category_agent_mapping",
            "type": "dictionary",
            "content": [
                "Credit Card Application",
                "Loan Approval Request",
                "Fraud / Dispute / Customer Support",
                "Credit Card Limit Extension / Due Date Change"
            ]
        }
    ]
}



@app.get("/.well-known/model-context.json")
def get_model_context():
    return JSONResponse(content=model_context)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=12001)

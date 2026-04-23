# fraud_mcp_server.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
import json
from litellm import completion
import requests

app = FastAPI()

# -------------------------------
# TOOL 1: Extract Fraud Details
# -------------------------------
def extract_fraud_details(email_data: dict) -> dict:
    """
    Extract fraud report information from structured email
    """

    prompt = f"""
You are given a structured email related to a fraud complaint.

Extract:

- full_name
- email
- contact_number
- account_number
- fraud_type
- transaction_details
- reported_date
- attachments

### Input:
{json.dumps(email_data, indent=2)}

### Output JSON:
{{
  "full_name": "",
  "email": "",
  "contact_number": null,
  "account_number": null,
  "fraud_type": "",
  "transaction_details": "",
  "reported_date": "",
  "attachments": []
}}

ONLY JSON.
"""

    try:
        response = completion(
            model="openrouter/openai/gpt-4-turbo",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response['choices'][0]['message']['content'])

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# TOOL 2: Check Missing Info
# -------------------------------
def check_missing_information(fraud_details: dict) -> dict:
    required_fields = ["full_name", "email", "fraud_type", "reported_date"]

    missing = [f for f in required_fields if not fraud_details.get(f)]

    return {
        "is_complete": len(missing) == 0,
        "missing_fields": missing
    }


# -------------------------------
# TOOL 3: Log Fraud Report
# -------------------------------
def log_fraud_report(fraud_details: dict) -> dict:

    response = requests.post(
        "http://localhost:8000/fraud-report",
        json=fraud_details
    )

    if response.status_code == 200:
        return {"message": "Fraud report logged successfully"}
    else:
        return {"error": response.text}


# -------------------------------
# MCP Context
# -------------------------------
model_context = {
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Processes fraud complaint emails by extracting details and logging them."
        },
        {
            "name": "functions",
            "type": "function",
            "content": [
                {
                    "name": "extract_fraud_details",
                    "description": "Extracts fraud complaint data from email",
                    "inputs": ["email_data"],
                    "output": "fraud_details"
                },
                {
                    "name": "check_missing_information",
                    "description": "Checks required fraud fields",
                    "inputs": ["fraud_details"],
                    "output": "status"
                },
                {
                    "name": "log_fraud_report",
                    "description": "Logs fraud report into DB",
                    "inputs": ["fraud_details"],
                    "output": "log_status"
                }
            ]
        }
    ]
}

@app.get("/.well-known/model-context.json")
def get_model_context():
    return JSONResponse(content=model_context)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=12003)
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
from google.adk.models.lite_llm import LiteLlm
from litellm import completion 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests


app = FastAPI()
import json

def extract_application_details(email_data: dict) -> dict:
    """
    Extracts essential applicant information from the email using LLM for parsing.
    """

    prompt = f"""
You are provided with a structured email in JSON format related to a credit card application.

Your task is to extract the following applicant information from the `body` of the email and any metadata:
- full_name: Full name of the applicant (can be derived from the sender email or body if mentioned)
- email: The sender's email address
- contact_number: Phone number (if mentioned)
- address: Address of the applicant (if mentioned)
- employment_type: One of [Salaried, Self-employed, Student, Retired, Other]
- monthly_income: Numeric income value or 'Unknown' if not provided
- existing_credit_card: 'Yes' or 'No'
- requested_credit_limit: Mentioned amount if any, else 'Not specified'
- attachments: List of filenames from the email attachments

### Input Email JSON:
{json.dumps(email_data, indent=2)}

### Output Strict JSON Format:
{{
    "full_name": "<Full Name>",
    "email": "<Email>",
    "contact_number": "<Phone Number or null>",
    "address": "<Address or null>",
    "employment_type": "<Employment Type>",
    "monthly_income": "<Income or 'Unknown'>",
    "existing_credit_card": "<Yes/No>",
    "requested_credit_limit": "<Limit or 'Not specified'>",
    "attachments": <List of attachment file names>
}}

Strictly output only the JSON object. Do not include any explanation.
"""
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



def check_missing_information(application_details: dict) -> dict:
    """
    Checks for any missing essential fields in the extracted application details.
    """
    required_fields = ["full_name", "email", "employment_type", "monthly_income"]
    
    missing = [field for field in required_fields if not application_details.get(field)]

    return {
        "is_complete": len(missing) == 0,
        "missing_fields": missing
    }

def log_credit_card_application(application_details: dict) -> dict:
    """
    Logs the complete application to the database via an API call.
    """
    api_url = "http://localhost:8000/credit-application"
    
    response = requests.post(api_url, json=application_details)

    if response.status_code == 200:
        return {"message": "Application logged successfully", "data": response.json()}
    else:
        return {"error": "Failed to log application", "details": response.text}


model_context={
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Processes credit card applications by extracting applicant details, checking completeness, logging to DB, and requesting missing info if needed."
        },
        {
            "name": "functions",
            "type": "function",
            "content": [
                {
                    "name": "extract_application_details",
                    "description": "Extracts relevant details from the email for credit card application.",
                    "inputs": ["email_data"],
                    "output": "application_details"
                },
                {
                    "name": "check_missing_information",
                    "description": "Checks whether required fields are present in the application details.",
                    "inputs": ["application_details"],
                    "output": "completeness_status"
                },
                {
                    "name": "log_credit_card_application",
                    "description": "Logs the application into the bank's credit card database.",
                    "inputs": ["application_details"],
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
    uvicorn.run(app, host="localhost", port=12002)

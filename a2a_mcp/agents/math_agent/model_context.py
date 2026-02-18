from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app = FastAPI()


def add_numbers(number1: float, number2: float) -> float:
    """ Adds the two numbers provided to it and returns the result back."""

    print("Using add tool from mcp")
    return number1 + number2

def subtract_numbers(number1: float, number2: float) -> float:
    """Subtracts the two numbers provided to it and returns back the result"""

    print("Using subtract tool from mcp")
    return number1 - number2


model_context = {
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Performs simple math operations like addition and subtraction."
        },
        {
            "name": "functions",
            "type": "function",
            "content": [
                {
                    "name": "add_numbers",
                    "description": "Adds two numbers and returns the result.",
                    "inputs": ["number1", "number2"],
                    "output": "sum"
                },
                {
                    "name": "subtract_numbers",
                    "description": "Subtracts the second number from the first.",
                    "inputs": ["number1", "number2"],
                    "output": "difference"
                }
            ]
        }
    ]
}

@app.get("/.well-known/model-context.json")
def get_model_context():
    return JSONResponse(content=model_context)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=11002)

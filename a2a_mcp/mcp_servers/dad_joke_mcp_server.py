from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app = FastAPI()

model_context = {
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Specializes in telling dad jokes, optionally based on a given topic."
        },
        {
            "name": "functions",
            "type": "function",
            "content": [
                {
                    "name": "tell_joke",
                    "description": "Provides a dad joke. Optionally accepts a topic to customize the joke.",
                    "inputs": ["topic"],
                    "output": "joke_text"
                }
            ]
        }
    ]
}

@app.get("/.well-known/model-context.json")
def get_model_context():
    return JSONResponse(content=model_context)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=11001)
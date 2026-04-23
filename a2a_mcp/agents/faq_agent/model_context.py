from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os
from litellm import completion

app = FastAPI()

# -------------------------------
# RULE-BASED FAQ KNOWLEDGE BASE
# -------------------------------
FAQ_DB = {
    "apply_credit_card": {
        "patterns": [
            "apply for credit card",
            "get a credit card",
            "credit card application",
            "how to apply credit card"
        ],
        "answer": "You can apply for a credit card by submitting an application via email or through our official website."
    },
    "min_income": {
        "patterns": [
            "minimum income",
            "salary requirement",
            "income needed for credit card"
        ],
        "answer": "The minimum income requirement for a credit card is typically ₹25,000 per month."
    },
    "report_fraud": {
        "patterns": [
            "report fraud",
            "unauthorized transaction",
            "fraud complaint",
            "suspicious transaction"
        ],
        "answer": "You can report fraud by emailing us with transaction details, your account number, and supporting documents."
    },
    "credit_limit": {
        "patterns": [
            "credit limit",
            "what is limit",
            "card limit"
        ],
        "answer": "The credit limit is the maximum amount you can spend using your credit card."
    },
    "approval_time": {
        "patterns": [
            "approval time",
            "how long approval",
            "processing time"
        ],
        "answer": "Credit card approval usually takes 5–7 working days."
    }
}


# -------------------------------
# TOOL: HYBRID FAQ ANSWER
# -------------------------------
def get_faq_answer(user_query: str) -> dict:
    query = user_query.lower()

    # ---- STEP 1: RULE MATCHING ----
    for faq in FAQ_DB.values():
        for pattern in faq["patterns"]:
            if pattern in query:
                return {
                    "answer": faq["answer"],
                    "source": "rule_based"
                }

    # ---- STEP 2: LLM FALLBACK ----
    prompt = f"""
You are a banking support assistant.

Answer the user's question clearly and concisely.

Guidelines:
- Only answer banking-related queries
- If unsure, say: "Please contact customer support for accurate information."
- Do NOT hallucinate policies
- Keep answer short and professional

User Query:
{user_query}

Answer:
"""

    try:
        response = completion(
            model="openrouter/openai/gpt-4-turbo",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response['choices'][0]['message']['content']

        return {
            "answer": answer.strip(),
            "source": "llm_fallback"
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# MCP CONTEXT
# -------------------------------
model_context = {
    "version": "v1",
    "context": [
        {
            "name": "agent_capability",
            "type": "text",
            "content": "Answers banking FAQs using hybrid rule-based + LLM approach."
        },
        {
            "name": "functions",
            "type": "function",
            "content": [
                {
                    "name": "get_faq_answer",
                    "description": "Returns FAQ answer using rule match or LLM fallback",
                    "inputs": ["user_query"],
                    "output": "answer"
                }
            ]
        }
    ]
}


@app.get("/.well-known/model-context.json")
def get_model_context():
    return JSONResponse(content=model_context)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=12004)
from fastapi import FastAPI, Body
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

client = MongoClient("mongodb+srv://my_database:helloworld@cluster0.oudn3ku.mongodb.net/")
db = client["bank_emails"]
credit_applications = db["credit_applications"]

class CreditApplication(BaseModel):
    full_name: str
    email: str
    contact_number: str | None = None
    address: str | None = None
    employment_type: str | None = None
    monthly_income: str | None = None
    existing_credit_card: str | None = None
    requested_credit_limit: str | None = None
    attachments: list[str] = []

@app.post("/credit-application")
def create_credit_application(app_data: CreditApplication):
    result = credit_applications.insert_one(app_data.model_dump())
    return {"status": "success", "inserted_id": str(result.inserted_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)

from pymongo import MongoClient
from faker import Faker

client = MongoClient("mongodb+srv://my_database:helloworld@cluster0.oudn3ku.mongodb.net/")
db = client["bank_emails"]
faker = Faker()

def seed_credit_card_applications(n=20):
    data = []
    for _ in range(n):
        data.append({
            "applicant_name": faker.name(),
            "email": faker.email(),
            "application_date": faker.date_time_this_year(),
            "status": "Pending",
            "attachments": ["PAN_Card.pdf", "Address_Proof.pdf"]
        })
    db.credit_card_applications.insert_many(data)

def seed_loan_requests(n=20):
    data = []
    for _ in range(n):
        data.append({
            "customer_name": faker.name(),
            "email": faker.email(),
            "loan_amount": faker.random_int(50000, 500000),
            "purpose": faker.sentence(),
            "status": "Pending"
        })
    db.loan_requests.insert_many(data)

def seed_support_tickets(n=20):
    data = []
    for _ in range(n):
        data.append({
            "customer_name": faker.name(),
            "email": faker.email(),
            "issue": faker.sentence(),
            "status": "Open"
        })
    db.support_tickets.insert_many(data)

def seed_limit_extensions(n=20):
    data = []
    for _ in range(n):
        data.append({
            "customer_name": faker.name(),
            "email": faker.email(),
            "current_limit": faker.random_int(50000, 200000),
            "requested_limit": faker.random_int(200000, 500000),
            "status": "Pending"
        })
    db.limit_extensions.insert_many(data)

if __name__ == "__main__":
    seed_credit_card_applications()
    seed_loan_requests()
    seed_support_tickets()
    seed_limit_extensions()
    print("Synthetic data seeded successfully.")

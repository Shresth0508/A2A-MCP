import requests
import os
from dotenv import load_dotenv
load_dotenv()

def search_trending_tech(domain: str, num_results: int) -> str:
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return "Serper API key not set."

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    query = f"latest trends in {domain}"
    payload = {
        "q": query,
        "num": num_results
    }

    response = requests.post(
        "https://google.serper.dev/search", json=payload, headers=headers
    )

    if response.status_code != 200:
        return f"Error fetching data: {response.text}"

    results = response.json().get("organic", [])
    if not results:
        return "No results found."

    summary = ""
    for i, item in enumerate(results, 1):
        summary += f"{i}. {item['title']}\n{item['link']}\n\n"

    return summary.strip()
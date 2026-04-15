import asyncio
import time
import json
import numpy as np
from clients.a2a_tool_client import A2AToolClient

# --- CONFIG ---
EMAIL_AGENT_URL = "http://localhost:10022"  # Email Categorizer
DATASET_PATH = "email_dataset.json"

# --- INIT CLIENT ---
a2a_client = A2AToolClient()

# --- METRIC STORAGE ---
simple_latencies = []
complex_latencies = []

simple_response_sizes = []
complex_response_sizes = []

all_latencies = []
complexity_labels = []  # 0 = simple, 1 = complex


# --- P95 FUNCTION ---
def compute_p95(data):
    return np.percentile(data, 95) if len(data) > 0 else 0


# --- PROCESS EMAIL ---
async def process_email(email):
    prompt = f"please categorize this email for me {json.dumps(email)}"

    start = time.perf_counter()
    response = await a2a_client.create_task(EMAIL_AGENT_URL, prompt)
    latency = time.perf_counter() - start

    response_size = len(response)

    return latency, response_size


# --- MAIN EXPERIMENT ---
async def run_experiment():
    with open(DATASET_PATH, "r") as f:
        dataset = json.load(f)

    print(f"🚀 Running experiment on {len(dataset)} emails...\n")

    for email in dataset:
        latency, response_size = await process_email(email)

        category = email["category"]

        # Store per category
        if category == "simple":
            simple_latencies.append(latency)
            simple_response_sizes.append(response_size)
            complexity_labels.append(0)
        else:
            complex_latencies.append(latency)
            complex_response_sizes.append(response_size)
            complexity_labels.append(1)

        all_latencies.append(latency)

        print(f"{email['id']} | {category} | {latency:.3f}s | size={response_size}")


# --- METRIC CALCULATION ---
def compute_stats(latencies, sizes):
    if len(latencies) == 0:
        return {}

    return {
        "count": len(latencies),
        "avg_latency": float(np.mean(latencies)),
        "median_latency": float(np.median(latencies)),
        "p95_latency": float(compute_p95(latencies)),
        "stddev_latency": float(np.std(latencies)),
        "avg_response_size": float(np.mean(sizes))
    }


def compute_correlation():
    if len(all_latencies) < 2:
        return 0
    return float(np.corrcoef(complexity_labels, all_latencies)[0, 1])


# --- RUN EVERYTHING ---
async def main():
    await run_experiment()

    results = {
        "simple": compute_stats(simple_latencies, simple_response_sizes),
        "complex": compute_stats(complex_latencies, complex_response_sizes),
        "overall": {
            "total_requests": len(all_latencies),
            "correlation_complexity_latency": compute_correlation()
        }
    }

    print("\n📊 FINAL RESULTS:\n")
    print(json.dumps(results, indent=2))

    # Save results to file (for paper/graphs)
    with open("experiment_complexity_results.json", "w") as f:
        json.dump(results, f, indent=2)


# --- ENTRY POINT ---
if __name__ == "__main__":
    asyncio.run(main())
# import threading
# import asyncio
# import time
# import uvicorn
# import nest_asyncio
# import sys
# import os
# import json

# # Ensure import path is correct
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # --- Local imports ---
# from servers.dad_joke_agent_server import create_dad_joke_agent_server
# from servers.email_agent_server import create_email_agent_server
# from servers.tech_trend_agent_server import create_tech_trend_agent_server
# from servers.host_agent_server import create_host_agent_server
# from servers.math_agent_server import create_math_agent_server
# from servers.Email_reciever_agent_server import create_email_receiver_agent_server
# from servers.Email_Categorizer_server import create_email_categorizer_agent_server
# from servers.credit_application_server import create_credit_application_agent_server
# from clients.a2a_tool_client import A2AToolClient

# nest_asyncio.apply()

# servers = []

# # --- Agent launching logic ---

# async def run_server(create_agent_function, port):
#     """Run server with proper error handling."""
#     try:
#         print(f"🚀 Starting agent on port {port}...")
#         app = create_agent_function()
#         config = uvicorn.Config(
#             app.build(),
#             host="127.0.0.1",
#             port=port,
#             log_level="info"
#         )
#         server = uvicorn.Server(config)
#         servers.append(server)
#         await server.serve()
#     except Exception as e:
#         print(f"❌ Agent error on port {port}: {e}")

# def run_agent_in_background(create_agent_function, port, name , **kwargs):
#     """Run an agent server in a background thread."""
#     def run():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         try:
#             loop.run_until_complete(run_server(create_agent_function, port))
#         except Exception as e:
#             print(f"{name} error: {e}")

#     thread = threading.Thread(target=run, daemon=True)
#     thread.start()
#     return thread

# # --- Start servers ---

# print("🔁 Launching agents...\n")

# # dad_joke_thread = run_agent_in_background(create_dad_joke_agent_server, 10020, "Dad Joke Agent",mcp_url="http://localhost:11001")
# # # email_agent_thread=run_agent_in_background(create_email_agent_server,10021,"Email Agent")
# # # tech_agent_thread=run_agent_in_background(create_tech_trend_agent_server,10023,"Tech trend Agent")
# # host_thread = run_agent_in_background(create_host_agent_server, 10022, "Host Agent",mcp_url="http:localhost:11000")
# dad_joke_thread = run_agent_in_background(
#     lambda: create_dad_joke_agent_server(mcp_url="http://localhost:11001"),
#     10020,
#     "Dad Joke Agent"
# )

# host_thread = run_agent_in_background(
#     lambda: create_host_agent_server(mcp_url="http://localhost:11000"),
#     10022,
#     "Host Agent"
# )
# math_agent_tread=run_agent_in_background(
#     lambda : create_math_agent_server(mcp_url="http://localhost:11002"),
#     10024,
#     "Math Agent"
# )

# email_reciever_thread=run_agent_in_background(
#     lambda : create_email_receiver_agent_server(mcp_url="http://localhost:12000"),
#     10025,
#     "Email Reciever Agent"
# )

# email_categorizer_thread=run_agent_in_background(
#     lambda : create_email_categorizer_agent_server(mcp_url="http://localhost:12001"),
#     10026,
#     "Email Categorizer Agent"
# )

# credit_application_thread=run_agent_in_background(
#     lambda : create_credit_application_agent_server(mcp_url="http://localhost:12002"),
#     10027,
#     "Credit Application Agent"
# )
# time.sleep(5)  # wait a few seconds to ensure servers are live

# # --- Register & Test Communication ---
# print("\n🔍 Registering remote agents and testing communication...\n")

# a2a_client = A2AToolClient()
# a2a_client.add_remote_agent("http://localhost:10020")  # dad joke
# # a2a_client.add_remote_agent("http://localhost:10021")  #email writer 
# a2a_client.add_remote_agent("http://localhost:10022")  # host agent
# # a2a_client.add_remote_agent("http://localhost:10023")  #tech_trend_agent
# a2a_client.add_remote_agent("http://localhost:10024") # math_agent
# a2a_client.add_remote_agent("http://localhost:10025")
# a2a_client.add_remote_agent("http://localhost:10026")
# a2a_client.add_remote_agent("http://localhost:10027") #credit application agent 

# # Test agent discovery
# remote_agents = a2a_client.list_remote_agents()
# for agent in remote_agents:
#     print(f"Remote agent name: {agent['name']}")
#     print(f"Remote agent url: {agent['url'] if 'url' in agent else 'unknown'}")
#     print(f"Remote agent skills: {agent['skills']}")
#     print(f"Remote agent version: {agent['version']}")
#     print("----\n")


# # --- Test direct communication (async block in sync script) ---
# async def compare_requests():
#     """Compare sequential vs parallel request processing using email dataset."""
#     # Load email dataset
#     with open("email_dataset.json", "r") as f:
#         email_dataset = json.load(f)

#     # Build requests from dataset (send to Email Categorizer)
#     requests_to_run = []
#     for email in email_dataset:
#         prompt = f"please categorize this email for me {json.dumps(email)}"
#         requests_to_run.append(("http://localhost:10022", prompt))  # Email Categorizer URL

#     print("=== Sequential Execution ===")
#     seq_start = time.perf_counter()
#     for url, prompt in requests_to_run:
#         response = await a2a_client.create_task(url, prompt)
#         print(f"{url} -> {response[:100]}...")
#     seq_duration = time.perf_counter() - seq_start
#     print(f"Sequential total time: {seq_duration:.2f} seconds\n")

#     print("=== Parallel Execution ===")
#     par_start = time.perf_counter()
#     tasks = [asyncio.create_task(a2a_client.create_task(url, prompt))
#              for url, prompt in requests_to_run]
#     responses = await asyncio.gather(*tasks)
#     par_duration = time.perf_counter() - par_start
#     print(f"Parallel total time: {par_duration:.2f} seconds\n")
#     for url, response in zip([r[0] for r in requests_to_run], responses):
#         print(f"{url} -> {response[:100]}...")

# async def test_direct_communication():
#     print("\n🎯 Testing direct agent calls...\n")

#     # Test dad joke agent
#     # dad_joke_response = await a2a_client.create_task("http://localhost:10020", "Tell me a joke about computers.")
#     # print("🧠 Dad Joke Agent Response:\n", dad_joke_response)

#     # Test host agent orchestration
#     # prompt=input("What do you want to do ? - ")
#     # host_response = await a2a_client.create_task(
#     #     "http://localhost:10022",
#     #     prompt
#     # )
#     # print("🧠 Host Agent Response:\n", host_response)
#     print("\n💬 Enter your request to the Host Agent (type 'quit' to exit):")

#     while True:
#         user_input = input("🧑 You: ")
#         if user_input.lower() in ["quit", "exit"]:
#             print("👋 Exiting...")
#             break

#         host_response = await a2a_client.create_task(
#             "http://localhost:10022",
#             user_input
#         )
#         print("🤖 Host Agent Response:\n", host_response)


# # Run async test block inside sync script
# asyncio.run(compare_requests())
# asyncio.run(test_direct_communication())


# import threading
# import asyncio
# import time
# import uvicorn
# import nest_asyncio
# import sys
# import os
# import json

# # Ensure import path is correct
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# # --- Local imports ---
# from servers.dad_joke_agent_server import create_dad_joke_agent_server
# from servers.email_agent_server import create_email_agent_server
# from servers.tech_trend_agent_server import create_tech_trend_agent_server
# from servers.host_agent_server import create_host_agent_server
# from servers.math_agent_server import create_math_agent_server
# from servers.Email_reciever_agent_server import create_email_receiver_agent_server
# from servers.Email_Categorizer_server import create_email_categorizer_agent_server
# from servers.credit_application_server import create_credit_application_agent_server

# # --- NEW: Fraud Agent Import ---
# from servers.fraud_reporting_agent_server import create_fraud_reporting_agent_server

# # --- NEW: Fraud MCP Import ---
# # from mcp_servers.fraud_mcp_server import app as fraud_mcp_app

# from clients.a2a_tool_client import A2AToolClient

# nest_asyncio.apply()

# servers = []

# # --- Agent launching logic ---

# async def run_server(create_agent_function, port):
#     """Run server with proper error handling."""
#     try:
#         print(f"🚀 Starting agent on port {port}...")
#         app = create_agent_function()
#         config = uvicorn.Config(
#             app.build(),
#             host="127.0.0.1",
#             port=port,
#             log_level="info"
#         )
#         server = uvicorn.Server(config)
#         servers.append(server)
#         await server.serve()
#     except Exception as e:
#         print(f"❌ Agent error on port {port}: {e}")

# def run_agent_in_background(create_agent_function, port, name , **kwargs):
#     """Run an agent server in a background thread."""
#     def run():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         try:
#             loop.run_until_complete(run_server(create_agent_function, port))
#         except Exception as e:
#             print(f"{name} error: {e}")

#     thread = threading.Thread(target=run, daemon=True)
#     thread.start()
#     return thread


# # --- NEW: MCP launcher ---
# def run_mcp_in_background(app, port, name):
#     def run():
#         uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

#     thread = threading.Thread(target=run, daemon=True)
#     thread.start()
#     print(f"🧩 MCP Server '{name}' started on port {port}")
#     return thread


# # --- Start servers ---

# print("🔁 Launching agents...\n")

# dad_joke_thread = run_agent_in_background(
#     lambda: create_dad_joke_agent_server(mcp_url="http://localhost:11001"),
#     10020,
#     "Dad Joke Agent"
# )

# host_thread = run_agent_in_background(
#     lambda: create_host_agent_server(mcp_url="http://localhost:11000"),
#     10022,
#     "Host Agent"
# )

# math_agent_tread = run_agent_in_background(
#     lambda : create_math_agent_server(mcp_url="http://localhost:11002"),
#     10024,
#     "Math Agent"
# )

# email_reciever_thread = run_agent_in_background(
#     lambda : create_email_receiver_agent_server(mcp_url="http://localhost:12000"),
#     10025,
#     "Email Reciever Agent"
# )

# email_categorizer_thread = run_agent_in_background(
#     lambda : create_email_categorizer_agent_server(mcp_url="http://localhost:12001"),
#     10026,
#     "Email Categorizer Agent"
# )

# credit_application_thread = run_agent_in_background(
#     lambda : create_credit_application_agent_server(mcp_url="http://localhost:12002"),
#     10027,
#     "Credit Application Agent"
# )

# # --- NEW: Start Fraud MCP ---
# # fraud_mcp_thread = run_mcp_in_background(
# #     fraud_mcp_app,
# #     12003,
# #     "Fraud MCP"
# # )

# # --- NEW: Start Fraud Agent ---
# fraud_reporting_thread = run_agent_in_background(
#     lambda: create_fraud_reporting_agent_server(mcp_url="http://localhost:12003"),
#     10028,
#     "Fraud Reporting Agent"
# )

# time.sleep(5)  # wait a few seconds to ensure servers are live


# # --- Register & Test Communication ---
# print("\n🔍 Registering remote agents and testing communication...\n")

# a2a_client = A2AToolClient()

# a2a_client.add_remote_agent("http://localhost:10020")  # dad joke
# a2a_client.add_remote_agent("http://localhost:10022")  # host agent
# a2a_client.add_remote_agent("http://localhost:10024")  # math agent
# a2a_client.add_remote_agent("http://localhost:10025")  # email receiver
# a2a_client.add_remote_agent("http://localhost:10026")  # email categorizer
# a2a_client.add_remote_agent("http://localhost:10027")  # credit application agent

# # --- NEW: Register Fraud Agent ---
# a2a_client.add_remote_agent("http://localhost:10028")  # fraud reporting agent


# # Test agent discovery
# remote_agents = a2a_client.list_remote_agents()
# for agent in remote_agents:
#     print(f"Remote agent name: {agent['name']}")
#     print(f"Remote agent url: {agent['url'] if 'url' in agent else 'unknown'}")
#     print(f"Remote agent skills: {agent['skills']}")
#     print(f"Remote agent version: {agent['version']}")
#     print("----\n")


# # --- Test direct communication (async block in sync script) ---
# async def compare_requests():
#     """Compare sequential vs parallel request processing using email dataset."""
    
#     with open("email_dataset.json", "r") as f:
#         email_dataset = json.load(f)

#     requests_to_run = []
#     for email in email_dataset:
#         prompt = f"please categorize this email for me {json.dumps(email)}"
#         requests_to_run.append(("http://localhost:10022", prompt))  # Host Agent

#     print("=== Sequential Execution ===")
#     seq_start = time.perf_counter()
#     for url, prompt in requests_to_run:
#         response = await a2a_client.create_task(url, prompt)
#         print(f"{url} -> {response[:100]}...")
#     seq_duration = time.perf_counter() - seq_start
#     print(f"Sequential total time: {seq_duration:.2f} seconds\n")

#     print("=== Parallel Execution ===")
#     par_start = time.perf_counter()
#     tasks = [asyncio.create_task(a2a_client.create_task(url, prompt))
#              for url, prompt in requests_to_run]
#     responses = await asyncio.gather(*tasks)
#     par_duration = time.perf_counter() - par_start
#     print(f"Parallel total time: {par_duration:.2f} seconds\n")
#     for url, response in zip([r[0] for r in requests_to_run], responses):
#         print(f"{url} -> {response[:100]}...")


# async def test_direct_communication():
#     print("\n🎯 Testing direct agent calls...\n")

#     print("\n💬 Enter your request to the Host Agent (type 'quit' to exit):")

#     while True:
#         user_input = input("🧑 You: ")
#         if user_input.lower() in ["quit", "exit"]:
#             print("👋 Exiting...")
#             break

#         host_response = await a2a_client.create_task(
#             "http://localhost:10022",
#             user_input
#         )
#         print("🤖 Host Agent Response:\n", host_response)


# # Run async test block inside sync script
# asyncio.run(compare_requests())
# asyncio.run(test_direct_communication())


import threading
import asyncio
import time
import uvicorn
import nest_asyncio
import sys
import os
import json

# Ensure import path is correct
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# --- Local imports ---
from servers.dad_joke_agent_server import create_dad_joke_agent_server
from servers.email_agent_server import create_email_agent_server
from servers.tech_trend_agent_server import create_tech_trend_agent_server
from servers.host_agent_server import create_host_agent_server
from servers.math_agent_server import create_math_agent_server
from servers.Email_reciever_agent_server import create_email_receiver_agent_server
from servers.Email_Categorizer_server import create_email_categorizer_agent_server
from servers.credit_application_server import create_credit_application_agent_server

# --- Existing Fraud Agent ---
from servers.fraud_reporting_agent_server import create_fraud_reporting_agent_server

# --- NEW: FAQ Agent Imports ---
from servers.faq_agent_server import create_faq_agent_server
# from mcp_servers.faq_mcp_server import app as faq_mcp_app

from clients.a2a_tool_client import A2AToolClient

nest_asyncio.apply()

servers = []

# --- Agent launching logic ---

async def run_server(create_agent_function, port):
    """Run server with proper error handling."""
    try:
        print(f"🚀 Starting agent on port {port}...")
        app = create_agent_function()
        config = uvicorn.Config(
            app.build(),
            host="127.0.0.1",
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        servers.append(server)
        await server.serve()
    except Exception as e:
        print(f"❌ Agent error on port {port}: {e}")

def run_agent_in_background(create_agent_function, port, name , **kwargs):
    """Run an agent server in a background thread."""
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(run_server(create_agent_function, port))
        except Exception as e:
            print(f"{name} error: {e}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread


# --- MCP launcher ---
def run_mcp_in_background(app, port, name):
    def run():
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print(f"🧩 MCP Server '{name}' started on port {port}")
    return thread


# --- Start servers ---

print("🔁 Launching agents...\n")

dad_joke_thread = run_agent_in_background(
    lambda: create_dad_joke_agent_server(mcp_url="http://localhost:11001"),
    10020,
    "Dad Joke Agent"
)

host_thread = run_agent_in_background(
    lambda: create_host_agent_server(mcp_url="http://localhost:11000"),
    10022,
    "Host Agent"
)

math_agent_tread = run_agent_in_background(
    lambda : create_math_agent_server(mcp_url="http://localhost:11002"),
    10024,
    "Math Agent"
)

email_reciever_thread = run_agent_in_background(
    lambda : create_email_receiver_agent_server(mcp_url="http://localhost:12000"),
    10025,
    "Email Reciever Agent"
)

email_categorizer_thread = run_agent_in_background(
    lambda : create_email_categorizer_agent_server(mcp_url="http://localhost:12001"),
    10026,
    "Email Categorizer Agent"
)

credit_application_thread = run_agent_in_background(
    lambda : create_credit_application_agent_server(mcp_url="http://localhost:12002"),
    10027,
    "Credit Application Agent"
)

# --- Existing Fraud Agent ---
fraud_reporting_thread = run_agent_in_background(
    lambda: create_fraud_reporting_agent_server(mcp_url="http://localhost:12003"),
    10028,
    "Fraud Reporting Agent"
)

# --- NEW: Start FAQ MCP ---
# faq_mcp_thread = run_mcp_in_background(
#     faq_mcp_app,
#     12004,
#     "FAQ MCP"
# )

# --- NEW: Start FAQ Agent ---
faq_agent_thread = run_agent_in_background(
    lambda: create_faq_agent_server(mcp_url="http://localhost:12004"),
    10029,
    "FAQ Agent"
)

time.sleep(5)  # wait a few seconds to ensure servers are live


# --- Register & Test Communication ---
print("\n🔍 Registering remote agents and testing communication...\n")

a2a_client = A2AToolClient()

a2a_client.add_remote_agent("http://localhost:10020")  # dad joke
a2a_client.add_remote_agent("http://localhost:10022")  # host agent
a2a_client.add_remote_agent("http://localhost:10024")  # math agent
a2a_client.add_remote_agent("http://localhost:10025")  # email receiver
a2a_client.add_remote_agent("http://localhost:10026")  # email categorizer
a2a_client.add_remote_agent("http://localhost:10027")  # credit application agent
a2a_client.add_remote_agent("http://localhost:10028")  # fraud reporting agent

# --- NEW: Register FAQ Agent ---
a2a_client.add_remote_agent("http://localhost:10029")  # FAQ agent


# Test agent discovery
remote_agents = a2a_client.list_remote_agents()
for agent in remote_agents:
    print(f"Remote agent name: {agent['name']}")
    print(f"Remote agent url: {agent['url'] if 'url' in agent else 'unknown'}")
    print(f"Remote agent skills: {agent['skills']}")
    print(f"Remote agent version: {agent['version']}")
    print("----\n")


# --- Test direct communication ---
async def compare_requests():
    with open("email_dataset.json", "r") as f:
        email_dataset = json.load(f)

    requests_to_run = []
    for email in email_dataset:
        prompt = f"please categorize this email for me {json.dumps(email)}"
        requests_to_run.append(("http://localhost:10022", prompt))

    print("=== Sequential Execution ===")
    seq_start = time.perf_counter()
    for url, prompt in requests_to_run:
        response = await a2a_client.create_task(url, prompt)
        print(f"{url} -> {response[:100]}...")
    seq_duration = time.perf_counter() - seq_start
    print(f"Sequential total time: {seq_duration:.2f} seconds\n")

    print("=== Parallel Execution ===")
    par_start = time.perf_counter()
    tasks = [asyncio.create_task(a2a_client.create_task(url, prompt))
             for url, prompt in requests_to_run]
    responses = await asyncio.gather(*tasks)
    par_duration = time.perf_counter() - par_start
    print(f"Parallel total time: {par_duration:.2f} seconds\n")
    for url, response in zip([r[0] for r in requests_to_run], responses):
        print(f"{url} -> {response[:100]}...")


async def test_direct_communication():
    print("\n🎯 Testing direct agent calls...\n")

    print("\n💬 Enter your request to the Host Agent (type 'quit' to exit):")

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("👋 Exiting...")
            break

        host_response = await a2a_client.create_task(
            "http://localhost:10022",
            user_input
        )
        print("🤖 Host Agent Response:\n", host_response)


asyncio.run(compare_requests())
asyncio.run(test_direct_communication())
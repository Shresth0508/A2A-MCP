# clients/a2a_tool_client.py

import json
import uuid
from typing import Any

import httpx
import requests

from utils.metrics import metrics
import time

from a2a.client import A2AClient
from a2a.types import SendMessageRequest, AgentCard, MessageSendParams


class A2AToolClient:
    """Client to interact with remote A2A agents."""

    def __init__(self, default_timeout: float = 120.0):
        self._agent_info_cache: dict[str, dict[str, Any] | None] = {}
        self.default_timeout = default_timeout

    def add_remote_agent(self, agent_url: str):
        normalized_url = agent_url.rstrip('/')
        if normalized_url not in self._agent_info_cache:
            self._agent_info_cache[normalized_url] = None

    # def list_remote_agents(self) -> list[dict[str, Any]]:
    #     if not self._agent_info_cache:
    #         return []

    #     remote_agents_info = []
    #     for remote_connection in self._agent_info_cache:
    #         if self._agent_info_cache[remote_connection] is not None:
    #             agent_data = self._agent_info_cache[remote_connection]
    #         else:
    #             try:
    #                 response = requests.get(f"{remote_connection}/.well-known/agent.json")
    #                 agent_data = response.json()
    #                 self._agent_info_cache[remote_connection] = agent_data
    #             except Exception as e:
    #                 print(f"Failed to fetch agent info from {remote_connection}: {e}")
    #                 continue
            
    #         mcp_url = None
    #         try:
    #             extensions = agent_data.get("capabilities", {}).get("extensions", [])
    #             if extensions:
    #                 mcp_url = extensions[0].get("uri")
    #         except Exception as e:
    #             print(f"Error extracting mcp_url from agent data for {remote_connection}: {e}")
    #         # ✅ Embed the URL in the agent info dictionary
    #         agent_data["mcp_url"] = mcp_url
    #         agent_data["url"] = remote_connection
    #         remote_agents_info.append(agent_data)

    #     return remote_agents_info

    def list_remote_agents(self) -> list[dict[str, Any]]:
        start_total = time.perf_counter()

        if not self._agent_info_cache:
            return []

        remote_agents_info = []

        for remote_connection in self._agent_info_cache:
            start = time.perf_counter()

            if self._agent_info_cache[remote_connection] is not None:
                agent_data = self._agent_info_cache[remote_connection]
                source = "cache"
            else:
                try:
                    response = requests.get(f"{remote_connection}/.well-known/agent.json")
                    agent_data = response.json()
                    self._agent_info_cache[remote_connection] = agent_data
                    source = "network"
                except Exception as e:
                    print(f"Failed to fetch agent info from {remote_connection}: {e}")
                    continue

            latency = time.perf_counter() - start
            metrics.record(
                "agent_discovery_latency",
                latency,
                tags={"agent_url": remote_connection, "source": source}
            )

            # existing logic
            mcp_url = None
            try:
                extensions = agent_data.get("capabilities", {}).get("extensions", [])
                if extensions:
                    mcp_url = extensions[0].get("uri")
            except Exception as e:
                print(f"Error extracting mcp_url: {e}")

            agent_data["mcp_url"] = mcp_url
            agent_data["url"] = remote_connection
            remote_agents_info.append(agent_data)

        total_latency = time.perf_counter() - start_total
        metrics.record("agent_discovery_total_latency", total_latency)

        metrics.record("agent_count", len(remote_agents_info))

        return remote_agents_info
    
    # def fetch_mcp(self, mcp_url: str):
    #     """
    #     Fetches the MCP (Model Context Protocol) from a remote agent.

    #     Parameters:
    #         agent (str): The mcp server url for a particular agent.

    #     Returns:
    #         dict: The MCP JSON data, or None if fetch fails.
    #     """
        

    #     # agent_url = agent["url"]
    #     mcp_url = f"{mcp_url}/.well-known/model-context.json"
    #     print(f"Fetching MCP from {mcp_url}")
    #     response = requests.get(mcp_url)
    #     if response.status_code == 200:
    #         print(f"✅ Fetched MCP from {mcp_url}")
    #         return response.json()
    #     else:
    #         print(f"❌ Failed to fetch MCP from {mcp_url}")
    #         return None
    
    def fetch_mcp(self, mcp_url: str):
        start = time.perf_counter()

        mcp_url_full = f"{mcp_url}/.well-known/model-context.json"
        print(f"Fetching MCP from {mcp_url_full}")

        try:
            response = requests.get(mcp_url_full)

            latency = time.perf_counter() - start
            metrics.record(
                "mcp_retrieval_latency",
                latency,
                tags={"mcp_url": mcp_url}
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            latency = time.perf_counter() - start
            metrics.record(
                "mcp_retrieval_failure_latency",
                latency,
                tags={"mcp_url": mcp_url, "error": str(e)}
            )
            return None


        
    # async def create_task(self, agent_url: str, message: str) -> str:
    #     print(f"⚠️ [DEBUG] Trying to call agent at: {agent_url}")
    #     timeout_config = httpx.Timeout(
    #         timeout=self.default_timeout,
    #         connect=10.0,
    #         read=self.default_timeout,
    #         write=10.0,
    #         pool=5.0
    #     )

    #     async with httpx.AsyncClient(timeout=timeout_config) as httpx_client:
    #         if agent_url in self._agent_info_cache and self._agent_info_cache[agent_url] is not None:
    #             agent_card_data = self._agent_info_cache[agent_url]
    #         else:
    #             agent_card_response = await httpx_client.get(f"{agent_url}/.well-known/agent.json")
    #             agent_card_data = await agent_card_response.json()
    #             self._agent_info_cache[agent_url] = agent_card_data

    #         agent_card = AgentCard(**agent_card_data)

    #         client = A2AClient(
    #             httpx_client=httpx_client,
    #             agent_card=agent_card
    #         )

    #         send_message_payload = {
    #             'message': {
    #                 'role': 'user',
    #                 'parts': [{'kind': 'text', 'text': message}],
    #                 'messageId': uuid.uuid4().hex,
    #             }
    #         }

    #         request = SendMessageRequest(
    #             id=str(uuid.uuid4()),
    #             params=MessageSendParams(**send_message_payload)
    #         )

    #         response = await client.send_message(request)

    #         try:
    #             response_dict = response.model_dump(mode='json', exclude_none=True)
    #             if 'result' in response_dict and 'artifacts' in response_dict['result']:
    #                 artifacts = response_dict['result']['artifacts']
    #                 for artifact in artifacts:
    #                     if 'parts' in artifact:
    #                         for part in artifact['parts']:
    #                             if 'text' in part:
    #                                 return part['text']
    #             return json.dumps(response_dict, indent=2)

    #         except Exception as e:
    #             print(f"Error parsing response: {e}")
    #             return str(response)
            
        

    async def create_task(self, agent_url: str, message: str) -> str:
        start_total = time.perf_counter()

        print(f"⚠️ [DEBUG] Trying to call agent at: {agent_url}")

        timeout_config = httpx.Timeout(
            timeout=self.default_timeout,
            connect=10.0,
            read=self.default_timeout,
            write=10.0,
            pool=5.0
        )

        async with httpx.AsyncClient(timeout=timeout_config) as httpx_client:

            # --- Agent card fetch latency ---
            start_card = time.perf_counter()

            if agent_url in self._agent_info_cache and self._agent_info_cache[agent_url] is not None:
                agent_card_data = self._agent_info_cache[agent_url]
                source = "cache"
            else:
                agent_card_response = await httpx_client.get(f"{agent_url}/.well-known/agent.json")
                agent_card_data = agent_card_response.json()
                self._agent_info_cache[agent_url] = agent_card_data
                source = "network"

            metrics.record(
                "agent_card_fetch_latency",
                time.perf_counter() - start_card,
                tags={"agent_url": agent_url, "source": source}
            )

            agent_card = AgentCard(**agent_card_data)

            client = A2AClient(
                httpx_client=httpx_client,
                agent_card=agent_card
            )

            send_message_payload = {
                'message': {
                    'role': 'user',
                    'parts': [{'kind': 'text', 'text': message}],
                    'messageId': uuid.uuid4().hex,
                }
            }

            request = SendMessageRequest(
                id=str(uuid.uuid4()),
                params=MessageSendParams(**send_message_payload)
            )

            # --- Actual delegation latency ---
            start_call = time.perf_counter()
            response = await client.send_message(request)
            delegation_latency = time.perf_counter() - start_call

            metrics.record(
                "task_delegation_latency",
                delegation_latency,
                tags={"agent_url": agent_url}
            )

            total_latency = time.perf_counter() - start_total
            metrics.record(
                "task_total_latency",
                total_latency,
                tags={"agent_url": agent_url}
            )

            # --- existing parsing ---
            try:
                response_dict = response.model_dump(mode='json', exclude_none=True)

                if 'result' in response_dict and 'artifacts' in response_dict['result']:
                    for artifact in response_dict['result']['artifacts']:
                        for part in artifact.get('parts', []):
                            if 'text' in part:
                                return part['text']

                return json.dumps(response_dict, indent=2)

            except Exception as e:
                print(f"Error parsing response: {e}")
                return str(response)

    async def create_task_with_resolver(self, agent_id_or_url: str, message: str) -> str:
        """
        Resolve agent name like 'dad_joke_agent' or 'Dad Joke Agent' to actual URL and call create_task.
        """
        if not agent_id_or_url.startswith("http://") and not agent_id_or_url.startswith("https://"):
            # Resolve name to URL
            for agent in self.list_remote_agents():
                name_slug = agent.get("name", "").lower().replace(" ", "_")
                if agent_id_or_url.lower() in [name_slug, agent.get("name", "").lower()]:
                    agent_id_or_url = agent["url"]
                    break
            else:
                raise ValueError(f"Unknown agent identifier: {agent_id_or_url}")

        return await self.create_task(agent_id_or_url, message)

    def remove_remote_agent(self, agent_url: str):
        normalized_url = agent_url.rstrip('/')
        if normalized_url in self._agent_info_cache:
            del self._agent_info_cache[normalized_url]

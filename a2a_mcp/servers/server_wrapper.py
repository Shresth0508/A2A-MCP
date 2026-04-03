import asyncio

import uvicorn
import time
import uuid
from utils.metrics import metrics
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    MessageSendParams,
    Part,
    TaskState,
    TextPart,
    AgentExtension
)


from a2a.utils import new_agent_text_message, new_task
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# Generic A2A Executor for any ADK agent


class ADKAgentExecutor(AgentExecutor):
    def __init__(self, agent, status_message="Processing request...", artifact_name="response",mcp_url=None):
        """Initialize a generic ADK agent executor.
        
        Args:
            agent: The ADK agent instance
            status_message: Message to display while processing
            artifact_name: Name for the response artifact
        """
       

        self.agent = agent
        self.status_message = status_message
        self.artifact_name = artifact_name
        self.mcp_url=mcp_url
        print(f"Ruuning mcp server on  : {self.mcp_url}")
        self.runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
        #print(f"[ADKAgentExecutor] Initialized with MCP URL: {self.mcp_url}")

    async def cancel(self, task_id: str) -> None:
        """Cancel the execution of a specific task."""
        # Implementation for cancelling tasks

    # async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
    #     query = context.get_user_input()
    #     task = context.current_task or new_task(context.message)
    #     await event_queue.enqueue_event(task)

    #     updater = TaskUpdater(event_queue, task.id, task.contextId)

    #     try:
    #         # Update status with custom message
    #         await updater.update_status(
    #             TaskState.working,
    #             new_agent_text_message(self.status_message, task.contextId, task.id)
    #         )

    #         # Process with ADK agent
    #         session = await self.runner.session_service.create_session(
    #             app_name=self.agent.name,
    #             user_id="a2a_user",
    #             state={},
    #             session_id=task.contextId,
    #         )

    #         content = types.Content(
    #             role='user',
    #             parts=[types.Part.from_text(text=query)]
    #         )

    #         response_text = ""
    #         async for event in self.runner.run_async(
    #             user_id="a2a_user",
    #             session_id=session.id,
    #             new_message=content
    #         ):
    #             if event.is_final_response() and event.content and event.content.parts:
    #                 for part in event.content.parts:
    #                     if hasattr(part, 'text') and part.text:
    #                         response_text += part.text + '\n'
    #                     elif hasattr(part, 'function_call'):
    #                         # Log or handle function calls if needed
    #                         pass  # Function calls are handled internally by ADK

    #         # Add response as artifact with custom name
    #         await updater.add_artifact(
    #             [Part(root=TextPart(text=response_text))],
    #             name=self.artifact_name
    #         )

    #         await updater.complete()

    #     except Exception as e:
    #         await updater.update_status(
    #             TaskState.failed,
    #             new_agent_text_message(f"Error: {e!s}", task.contextId, task.id),
    #             final=True
    #         )
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        trace_id = uuid.uuid4().hex

        start_total = time.perf_counter()

        query = context.get_user_input()
        task = context.current_task or new_task(context.message)

        await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.contextId)

        try:
            # --- Mark task as working ---
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message, task.contextId, task.id)
            )

            # --- Start decision latency ---
            decision_start = time.perf_counter()

            session = await self.runner.session_service.create_session(
                app_name=self.agent.name,
                user_id="a2a_user",
                state={},
                session_id=task.contextId,
            )

            content = types.Content(
                role='user',
                parts=[types.Part.from_text(text=query)]
            )

            response_text = ""

            async for event in self.runner.run_async(
                user_id="a2a_user",
                session_id=session.id,
                new_message=content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text + '\n'
                        elif hasattr(part, 'function_call'):
                            pass  # handled internally

            decision_latency = time.perf_counter() - decision_start

            metrics.record(
                "agent_decision_latency",
                decision_latency,
                tags={
                    "agent": self.agent.name,
                    "trace_id": trace_id
                }
            )

            # --- Response size (useful for cost proxy) ---
            metrics.record(
                "agent_response_size",
                len(response_text),
                tags={"agent": self.agent.name}
            )

            # --- Add artifact ---
            await updater.add_artifact(
                [Part(root=TextPart(text=response_text))],
                name=self.artifact_name
            )

            await updater.complete()

            # --- Total latency ---
            total_latency = time.perf_counter() - start_total

            metrics.record(
                "agent_total_latency",
                total_latency,
                tags={
                    "agent": self.agent.name,
                    "trace_id": trace_id
                }
            )

            metrics.event(
                "agent_success",
                {
                    "agent": self.agent.name,
                    "trace_id": trace_id
                }
            )

        except Exception as e:
            total_latency = time.perf_counter() - start_total

            metrics.record(
                "agent_total_latency",
                total_latency,
                tags={
                    "agent": self.agent.name,
                    "trace_id": trace_id,
                    "status": "failed"
                }
            )

            metrics.event(
                "agent_failure",
                {
                    "agent": self.agent.name,
                    "trace_id": trace_id,
                    "error": str(e)
                }
            )

            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Error: {e!s}", task.contextId, task.id),
                final=True
            )

# Generic function to create an A2A server for any ADK agent
import json

def create_agent_a2a_server(
    agent,
    name,
    description,
    skills,
    host="localhost",
    port=10020,
    status_message="Processing request...",
    artifact_name="response",
    mcp_url=None
):
    """Create an A2A server for any ADK agent."""
    
    # Agent capabilities
    capabilities = AgentCapabilities(
        streaming=True,
        extensions=[AgentExtension(uri=mcp_url)] if mcp_url else None
    )
    print(f"type of mcp_url: {type(mcp_url)}, value: {mcp_url}")
    print(f"Setting extensions with mcp_url: {mcp_url}")
    # Agent card (metadata) with MCP URL in extensions
    agent_card = AgentCard(
        name=name,
        description=description,
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        capabilities=capabilities,
        skills=skills
    )
    # Create executor
    executor = ADKAgentExecutor(
        agent=agent,
        status_message=status_message,
        artifact_name=artifact_name,
        mcp_url=mcp_url
    )

    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    return A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

     
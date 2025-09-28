import asyncio
from temporalio.worker import Worker
from temporalio.client import Client

from workflow import HelloAgentWorkflow
from activities import simulate_llm_response

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="agent-task-queue",
        workflows=[HelloAgentWorkflow],
        activities=[simulate_llm_response],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

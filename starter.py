import asyncio
from temporalio.client import Client

async def main():
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233")

    # Start the workflow (calls HelloAgentWorkflow.run with "Neo")
    try:
        result = await client.execute_workflow(
            "HelloAgentWorkflow",               # workflow to call
            "Neo",                              # argument to workflow
            id="hello-agent-workflow-id-v2",    # unique ID
            task_queue="agent-task-queue",      # must match worker
        )
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'cause'):
            print(f"Cause: {e.cause}")
        if hasattr(e, 'inner') and e.inner:
            print(f"Inner error: {e.inner}")
        if hasattr(e, 'failure') and e.failure:
            print(f"Failure details: {e.failure}")

if __name__ == "__main__":
    asyncio.run(main())

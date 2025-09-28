import asyncio
import time
from temporalio.client import Client


async def main():
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233")

    # Get search query from user
    query = input("🔍 What would you like to search for? ").strip()

    if not query:
        print("❌ Please enter a search query.")
        return

    # Start the web search workflow
    try:
        print(f"🚀 Starting search for: {query}")
        result = await client.execute_workflow(
            "WebSearchAgentWorkflow",           # workflow to call
            query,                              # search query
            id=f"web-search-{int(time.time())}",  # unique ID
            task_queue="agent-task-queue",      # must match worker
        )

        print("\n" + "="*60)
        print("📋 SEARCH RESULTS")
        print("="*60)
        print(result)
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'cause'):
            print(f"Cause: {e.cause}")
        if hasattr(e, 'inner') and e.inner:
            print(f"Inner error: {e.inner}")
        if hasattr(e, 'failure') and e.failure:
            print(f"Failure details: {e.failure}")


if __name__ == "__main__":
    asyncio.run(main())

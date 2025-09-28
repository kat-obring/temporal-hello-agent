import pytest
import asyncio
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from temporalio.testing import WorkflowEnvironment  # noqa: E402
from temporalio.worker import Worker  # noqa: E402
from workflow import WebSearchAgentWorkflow  # noqa: E402
from activities import web_search, summarize_results  # noqa: E402


@pytest.mark.asyncio
async def test_web_search_workflow():
    """Test the web search workflow with a real
    search query using WorkflowEnvironment."""
    # Start an in-memory test environment
    async with await WorkflowEnvironment.start_time_skipping() as env:
        client = env.client

        # Start a worker with our workflows + activities
        worker = Worker(
            client,
            task_queue="test-task-queue",
            workflows=[WebSearchAgentWorkflow],
            activities=[web_search, summarize_results],
        )

        async with worker:
            # Test search query
            query = "Python Temporal workflow"

            print(f"🚀 Starting search for: {query}")

            # Start the web search workflow
            result = await client.execute_workflow(
                WebSearchAgentWorkflow.run,     # workflow to call
                query,                          # search query
                id=f"web-search-{int(time.time())}",  # unique ID
                task_queue="test-task-queue",   # must match worker
            )

            print("\n" + "="*60)
            print("📋 SEARCH RESULTS")
            print("="*60)
            print(result)
            print("="*60)

            # Assert that we got some results
            assert "Search Results for:" in result
            assert query in result
            assert "🔍" in result  # Should have search emoji


if __name__ == "__main__":
    # Allow running as standalone script for manual testing
    asyncio.run(test_web_search_workflow())

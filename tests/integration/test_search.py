import pytest
import asyncio
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from temporalio.client import Client  # noqa: E402


@pytest.mark.asyncio
async def test_web_search_workflow():
    """Test the web search workflow with a real search query."""
    # Connect to the Temporal server
    client = await Client.connect("localhost:7233")

    # Test search query
    query = "Python Temporal workflow"
    
    print(f"🚀 Starting search for: {query}")

    # Start the web search workflow
    try:
        result = await client.execute_workflow(
            "WebSearchAgentWorkflow",           # workflow to call
            query,                              # search query
            id=f"web-search-{int(time.time())}", # unique ID
            task_queue="agent-task-queue",      # must match worker
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
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")
        pytest.fail(f"Web search workflow failed: {e}")


if __name__ == "__main__":
    # Allow running as standalone script for manual testing
    asyncio.run(test_web_search_workflow())

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from workflow import HelloAgentWorkflow, WebSearchAgentWorkflow  # noqa: E402
from temporalio import workflow  # noqa: E402


# Fake activity for testing
async def fake_activity(name: str) -> str:
    return f"Mocked agent {name} reporting in."


# Fake flaky activity that always fails
async def fake_flaky_activity(name: str) -> str:
    raise RuntimeError("Simulated LLM failure!")


# Fake successful activity
async def fake_successful_activity(name: str) -> str:
    return f"🤖 Agent {name} says: 'Let me look that up for you...'"


@pytest.mark.asyncio
async def test_workflow_with_mocked_activity():
    # Start a test workflow environment
    async def run_workflow():
        # Patch workflow.execute_activity to use fake_activity
        return await HelloAgentWorkflow().run("Morpheus")

    # Monkeypatch the execute_activity call inside workflow
    orig_execute_activity = workflow.execute_activity
    # a[1] = "Morpheus"
    workflow.execute_activity = lambda *a, **k: fake_activity(a[1])

    try:
        result = await run_workflow()
        assert "Morpheus" in result
        assert "Mocked agent" in result
    finally:
        # Restore the original function to avoid side effects
        workflow.execute_activity = orig_execute_activity


@pytest.mark.asyncio
async def test_workflow_with_retry_logic():
    """Test that workflow handles flaky activity failures and continues."""
    # Track how many times activities are called
    flaky_call_count = 0
    successful_call_count = 0

    async def mock_flaky_activity(name: str) -> str:
        nonlocal flaky_call_count
        flaky_call_count += 1
        raise RuntimeError("Simulated LLM failure!")

    async def mock_successful_activity(name: str) -> str:
        nonlocal successful_call_count
        successful_call_count += 1
        return f"🤖 Agent {name} says: 'Let me look that up for you...'"

    # Mock workflow.execute_activity to route to our test functions
    orig_execute_activity = workflow.execute_activity

    async def mock_execute_activity(activity_name, *args, **kwargs):
        if activity_name == "flaky_activity":
            # Simulate retry behavior - call the function multiple times
            retry_policy = kwargs.get('retry_policy')
            max_attempts = retry_policy.maximum_attempts if retry_policy else 3

            for attempt in range(max_attempts):
                try:
                    return await mock_flaky_activity(*args)
                except Exception as e:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise e
                    # Continue to next attempt (simulating retry)
                    continue
        elif activity_name == "simulate_llm_response":
            return await mock_successful_activity(*args)
        else:
            raise ValueError(f"Unknown activity: {activity_name}")

    workflow.execute_activity = mock_execute_activity

    try:
        result = await HelloAgentWorkflow().run("Neo")

        # Verify the result
        assert "Neo" in result
        assert "🤖 Agent" in result

        # Verify flaky activity was called (should fail after retries)
        assert flaky_call_count >= 3  # should be retried at least 3 times

        # Verify successful activity was called
        assert successful_call_count == 1

    finally:
        # Restore the original function
        workflow.execute_activity = orig_execute_activity


@pytest.mark.asyncio
async def test_web_search_workflow_success():
    """Test the WebSearchAgentWorkflow with successful activities."""
    # Track activity calls
    web_search_call_count = 0
    summarize_call_count = 0
    
    async def mock_web_search(query: str):
        nonlocal web_search_call_count
        web_search_call_count += 1
        return [
            {
                "title": f"Search result for {query}",
                "snippet": f"This is a test result for {query}",
                "url": f"https://example.com/search?q={query}",
                "source": "Test Source"
            }
        ]
    
    async def mock_summarize_results(args: tuple):
        nonlocal summarize_call_count
        summarize_call_count += 1
        query, search_results = args
        return f"🔍 **Search Results for: {query}**\nFound {len(search_results)} results."
    
    # Mock workflow.execute_activity
    orig_execute_activity = workflow.execute_activity
    
    async def mock_execute_activity(activity_name, *args, **kwargs):
        if activity_name == "web_search":
            return await mock_web_search(*args)
        elif activity_name == "summarize_results":
            return await mock_summarize_results(*args)
        else:
            raise ValueError(f"Unknown activity: {activity_name}")
    
    workflow.execute_activity = mock_execute_activity
    
    try:
        # Test the workflow
        query = "Python Temporal"
        result = await WebSearchAgentWorkflow().run(query)
        
        # Verify the result
        assert isinstance(result, str)
        assert query in result
        assert "Search Results for:" in result
        
        # Verify activities were called
        assert web_search_call_count == 1
        assert summarize_call_count == 1
        
    finally:
        # Restore the original function
        workflow.execute_activity = orig_execute_activity


@pytest.mark.asyncio
async def test_web_search_workflow_search_failure():
    """Test the WebSearchAgentWorkflow when web search fails."""
    # Track activity calls
    web_search_call_count = 0
    summarize_call_count = 0
    
    async def mock_web_search_failure(query: str):
        nonlocal web_search_call_count
        web_search_call_count += 1
        raise Exception("Network error")
    
    async def mock_summarize_results(args: tuple):
        nonlocal summarize_call_count
        summarize_call_count += 1
        query, search_results = args
        return f"🔍 **Search Results for: {query}**\nFound {len(search_results)} results."
    
    # Mock workflow.execute_activity
    orig_execute_activity = workflow.execute_activity
    
    async def mock_execute_activity(activity_name, *args, **kwargs):
        if activity_name == "web_search":
            return await mock_web_search_failure(*args)
        elif activity_name == "summarize_results":
            return await mock_summarize_results(*args)
        else:
            raise ValueError(f"Unknown activity: {activity_name}")
    
    workflow.execute_activity = mock_execute_activity
    
    try:
        # Test the workflow
        query = "Python Temporal"
        result = await WebSearchAgentWorkflow().run(query)
        
        # Verify the error result
        assert isinstance(result, str)
        assert "Search failed" in result
        assert query in result
        assert "Network error" in result
        
        # Verify only web search was called (summarize should not be called)
        assert web_search_call_count == 1
        assert summarize_call_count == 0
        
    finally:
        # Restore the original function
        workflow.execute_activity = orig_execute_activity


@pytest.mark.asyncio
async def test_web_search_workflow_summarize_failure():
    """Test the WebSearchAgentWorkflow when summarize fails."""
    # Track activity calls
    web_search_call_count = 0
    summarize_call_count = 0
    
    async def mock_web_search(query: str):
        nonlocal web_search_call_count
        web_search_call_count += 1
        return [
            {
                "title": f"Search result for {query}",
                "snippet": f"This is a test result for {query}",
                "url": f"https://example.com/search?q={query}",
                "source": "Test Source"
            }
        ]
    
    async def mock_summarize_failure(args: tuple):
        nonlocal summarize_call_count
        summarize_call_count += 1
        raise Exception("Summary processing error")
    
    # Mock workflow.execute_activity
    orig_execute_activity = workflow.execute_activity
    
    async def mock_execute_activity(activity_name, *args, **kwargs):
        if activity_name == "web_search":
            return await mock_web_search(*args)
        elif activity_name == "summarize_results":
            return await mock_summarize_failure(*args)
        else:
            raise ValueError(f"Unknown activity: {activity_name}")
    
    workflow.execute_activity = mock_execute_activity
    
    try:
        # Test the workflow
        query = "Python Temporal"
        result = await WebSearchAgentWorkflow().run(query)
        
        # Verify the error result
        assert isinstance(result, str)
        assert "Search completed but summary failed" in result
        assert query in result
        assert "Summary processing error" in result
        
        # Verify both activities were called
        assert web_search_call_count == 1
        assert summarize_call_count == 1
        
    finally:
        # Restore the original function
        workflow.execute_activity = orig_execute_activity

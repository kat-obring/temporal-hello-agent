import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow import HelloAgentWorkflow  # noqa: E402
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
    
    def mock_execute_activity(activity_name, *args, **kwargs):
        if activity_name == "flaky_activity":
            return mock_flaky_activity(*args)
        elif activity_name == "simulate_llm_response":
            return mock_successful_activity(*args)
        else:
            raise ValueError(f"Unknown activity: {activity_name}")
    
    workflow.execute_activity = mock_execute_activity
    
    try:
        result = await HelloAgentWorkflow().run("Neo")
        
        # Verify the result
        assert "Neo" in result
        assert "🤖 Agent" in result
        
        # Verify flaky activity was called (should fail after retries)
        assert flaky_call_count > 0
        
        # Verify successful activity was called
        assert successful_call_count == 1
        
    finally:
        # Restore the original function
        workflow.execute_activity = orig_execute_activity

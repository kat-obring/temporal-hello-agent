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

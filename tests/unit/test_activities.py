import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from activities import simulate_llm_response  # noqa: E402


@pytest.mark.asyncio
async def test_simulate_llm_response():
    result = await simulate_llm_response("Trinity")
    assert "Trinity" in result
    assert "🤖 Agent" in result

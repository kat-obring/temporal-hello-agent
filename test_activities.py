import pytest
from activities import simulate_llm_response


@pytest.mark.asyncio
async def test_simulate_llm_response():
    result = await simulate_llm_response("Trinity")
    assert "Trinity" in result
    assert "🤖 Agent" in result

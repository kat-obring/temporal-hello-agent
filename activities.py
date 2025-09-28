import asyncio
from temporalio import activity


@activity.defn
async def simulate_llm_response(name: str) -> str:
    await asyncio.sleep(1)  # Simulate thinking
    return f"🤖 Agent {name} says: 'Let me look that up for you...'"


@activity.defn
async def flaky_activity(name: str) -> str:
    print(f"flaky_activity called with: {name}")
    await asyncio.sleep(0.5)
    raise RuntimeError("Simulated LLM failure!")

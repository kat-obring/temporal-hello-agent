import asyncio
from temporalio import activity

@activity.defn
async def simulate_llm_response(name: str) -> str:
    await asyncio.sleep(1)  # Simulate thinking
    return f"🤖 Agent {name} says: 'Let me look that up for you...'"
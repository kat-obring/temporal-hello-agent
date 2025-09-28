from temporalio import workflow
from datetime import timedelta

@workflow.defn
class HelloAgentWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        result = await workflow.execute_activity(
            "simulate_llm_response",
            name,
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        return result

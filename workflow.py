from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta


@workflow.defn
class HelloAgentWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # First try the flaky activity (this will fail and retry)
        try:
            await workflow.execute_activity(
                "flaky_activity",
                name,
                schedule_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_attempts=3,
                ),
            )
        except Exception as e:
            # Flaky activity failed after retries, continue anyway
            print(f"Flaky activity failed after retries: {e}")
            pass

        # Call the LLM response
        result = await workflow.execute_activity(
            "simulate_llm_response",
            name,
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        return result

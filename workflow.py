from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta


@workflow.defn
class WebSearchAgentWorkflow:
    @workflow.run
    async def run(self, query: str) -> str:
        """Search the web for a query and return a summary of results."""
        print(f"🚀 Starting web search workflow for: {query}")

        # Step 1: Search the web
        try:
            search_results = await workflow.execute_activity(
                "web_search",
                query,
                schedule_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=2),
                    maximum_attempts=3,
                ),
            )
        except Exception as e:
            print(f"❌ Web search failed: {e}")
            return f"❌ Search failed for '{query}': {str(e)}"

        # Step 2: Summarize the results
        try:
            summary = await workflow.execute_activity(
                "summarize_results",
                (query, search_results),
                schedule_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_attempts=2,
                ),
            )
            print(f"✅ Web search workflow completed for: {query}")
            return summary
        except Exception as e:
            print(f"❌ Summary failed: {e}")
            return (f"❌ Search completed but summary failed for '{query}': "
                    f"{str(e)}")


# Keep the old workflow for backward compatibility
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

import pytest
import asyncio
from temporalio.testing import WorkflowEnvironment
from temporalio.client import Client
from temporalio.worker import Worker

from workflow import HelloAgentWorkflow
from activities import simulate_llm_response, flaky_activity


@pytest.mark.asyncio
async def test_workflow_end_to_end_with_retries():
    # Start an in-memory test environment
    async with await WorkflowEnvironment.start_time_skipping() as env:
        client = env.client

        # Start a worker with our workflow + activities
        worker = Worker(
            client,
            task_queue="test-task-queue",
            workflows=[HelloAgentWorkflow],
            activities=[simulate_llm_response, flaky_activity],
        )

        async with worker:
            # Run the workflow through the real Temporal runtime
            result = await client.execute_workflow(
                HelloAgentWorkflow.run,
                "Trinity",
                id="test-workflow-id",
                task_queue="test-task-queue",
            )

            # Assert on the final result
            assert "🤖 Agent Trinity says:" in result

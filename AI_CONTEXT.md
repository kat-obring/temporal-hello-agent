# AI Context - Temporal Hello Agent

## Current State
- **Working Temporal project** with retry logic and error handling
- **Tests passing** - both activity and workflow tests with retry simulation
- **CI/CD setup** - GitHub Actions with branch protection
- **All linting clean** - flake8, black, autopep8 configured

## Key Files & Purpose
- `workflow.py` - Main workflow with retry logic (flaky_activity → simulate_llm_response)
- `activities.py` - Two activities: flaky (always fails), simulate_llm_response (success)
- `worker.py` - Registers activities and workflows
- `starter.py` - Client with unique workflow IDs (timestamp-based)
- `tests/test_workflow.py` - Mock-based tests with retry simulation

## Current Workflow Logic
```python
# workflow.py - HelloAgentWorkflow.run()
try:
    await workflow.execute_activity("flaky_activity", retry_policy=RetryPolicy(maximum_attempts=3))
except Exception as e:
    print(f"Flaky activity failed after retries: {e}")
    # Continue anyway

result = await workflow.execute_activity("simulate_llm_response", name)
return result
```

## Test Strategy
- **Mock `workflow.execute_activity`** to simulate Temporal behavior
- **Implement retry logic in mock** - call flaky activity 3 times before failing
- **Track call counts** - verify `flaky_call_count >= 3`
- **Async mocks** - `async def mock_execute_activity()`

## Recent Issues Fixed
1. **Import error**: `RetryPolicy` from `temporalio.common` not `temporalio.workflow`
2. **Activity names**: Use `"flaky_activity"` not `"activities.flaky_activity"`
3. **Unique workflow IDs**: Use `f"hello-agent-workflow-{int(time.time())}"`
4. **Test retry simulation**: Made mock async and implemented retry loop

## Commands
```bash
pipenv run test    # Run tests
pipenv run lint    # Check linting
pipenv run fix     # Auto-fix whitespace
pipenv run format  # Black formatting
```

## Project Structure
```
temporal_hello_agent/
├── activities.py, workflow.py, worker.py, starter.py
├── tests/test_activities.py, tests/test_workflow.py
├── Pipfile (with scripts), .github/workflows/ci.yml
└── README.md, CONTEXT.md, AI_CONTEXT.md
```

## Current Status
- ✅ All tests passing
- ✅ Linting clean
- ✅ CI/CD working
- ✅ Retry logic working
- ✅ Error handling working
- ✅ Unique workflow IDs working

## Next Steps
- Any enhancements or new features
- Additional test cases
- Documentation updates

# Temporal Hello Agent - Project Context

## Project Overview
A Temporal workflow example demonstrating AI agent simulation with retry logic and error handling. The project showcases Temporal's workflow and activity patterns with comprehensive testing and CI/CD.

## Architecture

### Core Components
- **Workflow**: `HelloAgentWorkflow` - Orchestrates agent interaction with retry logic
- **Activities**: 
  - `simulate_llm_response` - Simulates successful LLM response
  - `flaky_activity` - Simulates failing LLM that triggers retries
- **Client**: `starter.py` - Triggers workflow executions
- **Worker**: `worker.py` - Processes workflow and activity tasks

### Key Features
- **Retry Logic**: Flaky activity fails 3 times before workflow continues
- **Error Handling**: Graceful failure handling with try/catch
- **Unique Workflow IDs**: Timestamp-based IDs prevent conflicts
- **Comprehensive Testing**: Unit tests for activities and workflows

## Project Structure
```
temporal_hello_agent/
├── activities.py              # Activity functions
├── workflow.py                # Workflow definitions with retry logic
├── worker.py                  # Temporal worker
├── starter.py                 # Client to trigger workflows
├── tests/                     # Test directory
│   ├── __init__.py
│   ├── test_activities.py     # Activity unit tests
│   └── test_workflow.py       # Workflow unit tests with retry simulation
├── Pipfile                    # Dependencies and scripts
├── .github/workflows/ci.yml   # GitHub Actions CI/CD
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
└── CONTEXT.md                 # This file
```

## Dependencies

### Production
- `temporalio` - Temporal Python SDK

### Development
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `flake8` - Linting
- `black` - Code formatting
- `autopep8` - Auto-fix whitespace issues

## Available Scripts
```bash
pipenv run test        # Run tests with verbose output
pipenv run test-cov    # Run tests with coverage report
pipenv run lint        # Check code style with flake8
pipenv run format      # Format code with black
pipenv run fix         # Auto-fix whitespace issues with autopep8
```

## Workflow Logic

### Retry Behavior
1. **Flaky Activity**: Always fails with `RuntimeError`
2. **Retry Policy**: 3 attempts with 1-second intervals
3. **Error Handling**: Catches exception and continues
4. **Success Activity**: Runs after flaky activity fails

### Code Flow
```python
# workflow.py
try:
    await workflow.execute_activity("flaky_activity", ...)  # Fails 3 times
except Exception as e:
    print(f"Flaky activity failed after retries: {e}")
    # Continue anyway

result = await workflow.execute_activity("simulate_llm_response", ...)
return result
```

## Testing Strategy

### Activity Tests
- Direct function testing (bypasses Temporal decorators)
- Verifies return values and behavior

### Workflow Tests
- Mocks `workflow.execute_activity` to simulate Temporal behavior
- Tests retry logic by calling activities multiple times
- Verifies error handling and continuation
- Tracks call counts to ensure retry behavior

### Test Assertions
```python
# Verify retry behavior
assert flaky_call_count >= 3  # Should be retried at least 3 times

# Verify successful completion
assert successful_call_count == 1
assert "Neo" in result
assert "🤖 Agent" in result
```

## CI/CD Pipeline

### GitHub Actions
- **Triggers**: Push to main/develop, pull requests to main
- **Python Version**: 3.11
- **Steps**:
  1. Install pipenv and dependencies
  2. Run linting (flake8)
  3. Run tests (pytest)
  4. Run coverage tests

### Branch Protection
- **PR Required**: Yes (1 approval, self-approval allowed)
- **CI Required**: Must pass before merging
- **Linear History**: Required
- **Force Push**: Blocked on main
- **Deletions**: Restricted

## Development Workflow

### Running the Application
1. **Start Temporal Server**: `docker run -p 7233:7233 -p 8233:8233 temporalio/auto-setup:latest`
2. **Start Worker**: `pipenv run python worker.py` (Terminal 1)
3. **Run Starter**: `pipenv run python starter.py` (Terminal 2)

### Code Changes
- **Worker Restart Required**: After changes to workflow.py, activities.py, worker.py
- **No Restart Needed**: Changes to starter.py, tests

### Testing
- **Unit Tests**: `pipenv run test`
- **Linting**: `pipenv run lint`
- **Auto-fix**: `pipenv run fix`

## Key Learnings

### Temporal Concepts
- **Workflows**: Orchestrate business logic, must be deterministic
- **Activities**: Perform actual work, can fail and retry
- **Retry Policies**: Configure retry behavior (attempts, intervals)
- **Error Handling**: Catch exceptions to continue workflow execution

### Testing Patterns
- **Mock Temporal Functions**: Replace `workflow.execute_activity` for testing
- **Simulate Retry Logic**: Implement retry behavior in mocks
- **Track Call Counts**: Verify expected number of retry attempts
- **Async Testing**: Use `@pytest.mark.asyncio` for async functions

### Development Practices
- **Unique Workflow IDs**: Use timestamps to prevent conflicts
- **Proper Imports**: `RetryPolicy` from `temporalio.common`
- **Activity Names**: Match between workflow calls and worker registration
- **Error Logging**: Print exceptions for debugging

## Common Issues & Solutions

### "Workflow execution already started"
- **Cause**: Reusing workflow ID
- **Solution**: Use unique IDs (timestamp-based)

### "Activity not registered"
- **Cause**: Name mismatch between workflow and worker
- **Solution**: Use consistent activity names (no module prefixes)

### "RetryPolicy not found"
- **Cause**: Wrong import path
- **Solution**: Import from `temporalio.common`, not `temporalio.workflow`

### Test Failures
- **Mock Issues**: Ensure mocks are async and properly await calls
- **Retry Simulation**: Implement retry logic in mocks to match Temporal behavior

## Next Steps for Enhancement
- Add more sophisticated retry policies
- Implement circuit breaker patterns
- Add integration tests with real Temporal server
- Add monitoring and observability
- Implement workflow versioning
- Add more complex workflow patterns (parallel activities, timers, etc.)

## Environment Setup
```bash
# Install dependencies
pipenv install --dev

# Start Temporal server
docker run -p 7233:7233 -p 8233:8233 temporalio/auto-setup:latest

# Run tests
pipenv run test

# Run application
pipenv run python worker.py  # Terminal 1
pipenv run python starter.py # Terminal 2
```

This context file should help you quickly understand and resume work on this project! 🚀

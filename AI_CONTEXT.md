# AI Context - Temporal Hello Agent

## Current State
- **Working Temporal project** with two workflows: simple hello and web search
- **All tests passing** - unit tests (mocked) and integration tests (real Temporal)
- **CI/CD setup** - GitHub Actions with branch protection rules
- **Clean code** - flake8, black, autopep8 configured and passing
- **Web search functionality** - DuckDuckGo API integration with result summarization

## Key Files & Purpose
- `workflow.py` - Two workflows: `HelloAgentWorkflow` (retry demo) and `WebSearchAgentWorkflow` (web search)
- `activities.py` - Four activities: `flaky_activity`, `simulate_llm_response`, `web_search`, `summarize_results`
- `worker.py` - Registers all workflows and activities
- `hello_starter.py` - Client for simple hello workflow (tests retry logic)
- `web_search_starter.py` - Client for web search workflow (interactive search)
- `tests/unit/` - Mock-based unit tests
- `tests/integration/` - Real Temporal integration tests

## Workflow Logic

### HelloAgentWorkflow (Simple Retry Demo)
```python
try:
    await workflow.execute_activity("flaky_activity", retry_policy=RetryPolicy(maximum_attempts=3))
except Exception as e:
    print(f"Flaky activity failed after retries: {e}")
    # Continue anyway

result = await workflow.execute_activity("simulate_llm_response", name)
return result
```

### WebSearchAgentWorkflow (Web Search)
```python
# Step 1: Search the web
search_results = await workflow.execute_activity("web_search", query, retry_policy=RetryPolicy(maximum_attempts=3))

# Step 2: Summarize results
summary = await workflow.execute_activity("summarize_results", (query, search_results), retry_policy=RetryPolicy(maximum_attempts=2))
return summary
```

## Activities

### web_search(query: str) -> List[Dict[str, str]]
- Uses DuckDuckGo instant answer API
- Returns structured results with title, snippet, URL, source
- Handles errors gracefully with fallback results

### summarize_results(args: tuple) -> str
- Takes (query, search_results) as tuple
- Formats results into readable markdown-style summary
- Includes emojis, numbered results, and clickable URLs

## Test Strategy
- **Unit Tests** (`tests/unit/`): Mock `workflow.execute_activity` to simulate Temporal behavior
- **Integration Tests** (`tests/integration/`): Use real Temporal client and `WorkflowEnvironment`
- **Retry simulation**: Mock calls flaky activity 3 times before failing
- **Async mocks**: All test functions are async with proper mocking

## Recent Issues Fixed
1. **Import error**: `RetryPolicy` from `temporalio.common` not `temporalio.workflow`
2. **Activity names**: Use `"flaky_activity"` not `"activities.flaky_activity"`
3. **Activity arguments**: Pass multiple args as tuple `(query, search_results)` to `summarize_results`
4. **File naming**: Renamed `starter.py` → `hello_starter.py`, `search_starter.py` → `web_search_starter.py`
5. **Test structure**: Separated unit and integration tests into different directories

## Commands
```bash
pipenv run test              # Run all tests
pipenv run test-unit         # Run only unit tests (fast)
pipenv run test-integration  # Run only integration tests
pipenv run test-cov          # Run tests with coverage
pipenv run lint              # Check linting
pipenv run fix               # Auto-fix whitespace
pipenv run format            # Black formatting
```

## Project Structure
```
temporal_hello_agent/
├── activities.py              # All activity functions
├── workflow.py                # Workflow definitions
├── worker.py                  # Temporal worker
├── hello_starter.py           # Client for hello workflow
├── web_search_starter.py      # Client for web search workflow
├── tests/
│   ├── unit/
│   │   ├── test_activities.py
│   │   └── test_workflow_logic.py
│   └── integration/
│       ├── test_search.py
│       └── test_temporal_end_to_end.py
├── Pipfile                    # Dependencies and scripts
├── .github/workflows/ci.yml   # CI/CD pipeline
├── README.md                  # Documentation
├── CONTEXT.md                 # Detailed project context
└── AI_CONTEXT.md              # This file
```

## Current Status
- ✅ All tests passing (unit + integration)
- ✅ Linting clean
- ✅ CI/CD working with branch protection
- ✅ Retry logic working
- ✅ Web search functionality working
- ✅ Error handling working
- ✅ File structure organized
- ✅ Documentation updated

## Key Technical Details
- **Dependencies**: `temporalio`, `requests`, `beautifulsoup4`, `pytest`, `pytest-asyncio`
- **Activity argument passing**: Use tuples for multiple arguments
- **Retry policies**: Configured with `RetryPolicy(initial_interval, maximum_attempts)`
- **Error handling**: Graceful fallbacks for web search failures
- **Test environment**: Uses `WorkflowEnvironment` for integration tests

## Usage Examples
```bash
# Start worker
pipenv run python worker.py

# Test simple workflow (in another terminal)
pipenv run python hello_starter.py

# Test web search (in another terminal)
pipenv run python web_search_starter.py
```

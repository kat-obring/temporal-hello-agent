# Temporal Hello Agent

A simple Temporal workflow example that demonstrates an AI agent simulation using Temporal's workflow and activity patterns.

## Overview

This project showcases:
- **Workflow**: `HelloAgentWorkflow` - Orchestrates the agent interaction
- **Activity**: `simulate_llm_response` - Simulates an LLM response with a delay
- **Client**: `starter.py` - Triggers workflow executions
- **Worker**: `worker.py` - Processes workflow and activity tasks

## Prerequisites

- Python 3.11+
- pipenv
- Docker (for Temporal server)

## Setup

1. **Install dependencies:**
   ```bash
   pipenv install --dev
   ```

2. **Start Temporal server:**
   ```bash
   docker run -p 7233:7233 -p 8233:8233 temporalio/auto-setup:latest
   ```

## Development

### Available Commands

- `pipenv run test` - Run all tests with verbose output
- `pipenv run test-unit` - Run only unit tests
- `pipenv run test-integration` - Run only integration tests
- `pipenv run test-cov` - Run all tests with coverage report
- `pipenv run lint` - Check code style with flake8
- `pipenv run format` - Format code with black
- `pipenv run fix` - Auto-fix whitespace issues

### Running the Application

1. **Start the worker** (in one terminal):
   ```bash
   pipenv run python worker.py
   ```

2. **Run the starter** (in another terminal):
   ```bash
   pipenv run python starter.py
   ```

The worker will process the workflow and return: `🤖 Agent Neo says: 'Let me look that up for you...'`

## Project Structure

```
temporal_hello_agent/
├── activities.py      # Activity functions
├── workflow.py        # Workflow definitions
├── worker.py          # Temporal worker
├── starter.py         # Client to trigger workflows
├── test_activities.py # Tests for activities
├── Pipfile           # Dependencies
└── README.md         # This file
```

## How It Works

1. The `starter.py` client sends a workflow execution request to Temporal
2. The `worker.py` picks up the workflow task and starts executing `HelloAgentWorkflow`
3. The workflow calls the `simulate_llm_response` activity
4. The activity simulates thinking time and returns a response
5. The workflow completes and returns the result to the client

## Testing

### Test Types

**Unit Tests** (`tests/unit/`):
- Test individual activities and workflow logic
- Use mocks to simulate Temporal behavior
- Fast and don't require external dependencies

**Integration Tests** (`tests/integration/`):
- Test complete workflows with real Temporal runtime
- Use `WorkflowEnvironment` for in-memory testing
- Verify end-to-end behavior

### Running Tests

```bash
# Run all tests
pipenv run test

# Run only unit tests (fast)
pipenv run test-unit

# Run only integration tests
pipenv run test-integration

# Run with coverage
pipenv run test-cov
```

The tests verify retry logic, error handling, and expected response formats.

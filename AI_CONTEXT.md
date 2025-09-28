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

## LinkedIn Content Creation AI Agent - Next Development Phase

### **Current Project Status**
- ✅ **Solid Foundation**: Working Temporal workflows with web search and retry logic
- ✅ **Complete Test Coverage**: Unit and integration tests for all functionality
- ✅ **Clean Codebase**: All linting issues resolved, CI/CD pipeline working
- ✅ **Documentation**: Comprehensive README, CONTEXT.md, and AI_CONTEXT.md

### **Next Development Goal**
Transform the current web search agent into a **LinkedIn Content Creation AI Agent** that helps find interesting topics and write LinkedIn content.

### **Immediate Next Steps** (Ready to Implement)

1. **Create LinkedInContentWorkflow** - New workflow to orchestrate content creation
2. **Enhance web search** - Focus on LinkedIn-relevant topics and trending content
3. **Add content generation activity** - AI-powered LinkedIn post creation
4. **Add content optimization activity** - Format for LinkedIn's algorithm

### **Technical Implementation Plan**

**New Activities to Create:**
```python
# Enhanced topic research for LinkedIn
@activity.defn
async def research_linkedin_topics(query: str) -> List[Dict]:
    # Search for trending LinkedIn topics, competitor content, hashtags

# AI content generation
@activity.defn  
async def generate_linkedin_content(topic_data: List[Dict]) -> str:
    # Generate LinkedIn posts with hooks, value, story, CTA

# LinkedIn optimization
@activity.defn
async def optimize_linkedin_content(content: str) -> Dict:
    # Format for LinkedIn algorithm, add hashtags, optimize length
```

**New Workflow Structure:**
```python
@workflow.defn
class LinkedInContentWorkflow:
    @workflow.run
    async def run(self, topic_query: str, content_type: str) -> Dict:
        # Step 1: Research trending topics
        topics = await workflow.execute_activity("research_linkedin_topics", topic_query)
        
        # Step 2: Generate content  
        content = await workflow.execute_activity("generate_linkedin_content", topics)
        
        # Step 3: Optimize for LinkedIn
        optimized = await workflow.execute_activity("optimize_linkedin_content", content)
        
        return optimized
```

### **Dependencies to Add**
- `openai` - For AI content generation
- `linkedin-api` - For LinkedIn integration (future)
- `schedule` - For content scheduling (future)
- `pytz` - For timezone handling (future)

### **Development Phases**
1. **Phase 1**: Core content generation workflow (immediate focus)
2. **Phase 2**: User experience and workflow management
3. **Phase 3**: LinkedIn API integration and analytics
4. **Phase 4**: Advanced AI features and personalization

### **Key Files to Modify**
- `workflow.py` - Add `LinkedInContentWorkflow`
- `activities.py` - Add new LinkedIn-focused activities
- `worker.py` - Register new workflow and activities
- Create `linkedin_content_starter.py` - New client script

### **Testing Strategy**
- Follow existing pattern: unit tests with mocks + integration tests with `WorkflowEnvironment`
- Test each new activity individually
- Test complete workflow end-to-end
- Maintain existing test coverage

### **Current Working State**
- All 12 tests passing (unit + integration)
- Linting clean (flake8 passing)
- CI/CD pipeline working
- Ready for new feature development

### **Quick Start Commands**
```bash
# Run all tests to verify current state
pipenv run test

# Check linting
pipenv run lint

# Start development
pipenv run python worker.py  # Terminal 1
pipenv run python web_search_starter.py  # Terminal 2 (for testing)
```

### **Critical Technical Patterns & Gotchas**

**Activity Argument Passing:**
```python
# WRONG - Multiple positional args fail
await workflow.execute_activity("activity_name", arg1, arg2, arg3)

# CORRECT - Use tuple for multiple args
await workflow.execute_activity("activity_name", (arg1, arg2, arg3))

# Activity function signature
@activity.defn
async def my_activity(args: tuple) -> str:
    arg1, arg2, arg3 = args  # Unpack tuple
```

**Import Patterns:**
```python
# CORRECT imports
from temporalio.common import RetryPolicy  # NOT from temporalio.workflow
from temporalio.testing import WorkflowEnvironment  # For integration tests
```

**Activity Registration:**
```python
# Worker registration - use simple names, no module prefixes
activities=[simulate_llm_response, flaky_activity, web_search, summarize_results]

# Workflow calls - match exact names
await workflow.execute_activity("web_search", query)  # NOT "activities.web_search"
```

**Test Mocking Patterns:**
```python
# Unit tests - mock workflow.execute_activity
orig_execute_activity = workflow.execute_activity

async def mock_execute_activity(activity_name, *args, **kwargs):
    if activity_name == "flaky_activity":
        # Simulate retry behavior
        for attempt in range(max_attempts):
            try:
                return await mock_flaky_activity(*args)
            except Exception:
                if attempt == max_attempts - 1:
                    raise
    # ... other activities

workflow.execute_activity = mock_execute_activity
```

**Integration Test Pattern:**
```python
# Use WorkflowEnvironment for CI/CD compatibility
async with await WorkflowEnvironment.start_time_skipping() as env:
    client = env.client
    worker = Worker(client, task_queue="test-task-queue", 
                   workflows=[MyWorkflow], activities=[my_activity])
    async with worker:
        result = await client.execute_workflow(MyWorkflow.run, args, ...)
```

**Error Handling Pattern:**
```python
try:
    result = await workflow.execute_activity("activity", args, 
        retry_policy=RetryPolicy(initial_interval=timedelta(seconds=1), 
                                maximum_attempts=3))
except Exception as e:
    print(f"Activity failed: {e}")
    return f"Error: {str(e)}"  # Graceful fallback
```

**File Structure Rules:**
- `tests/unit/` - Mock-based tests, fast, no external dependencies
- `tests/integration/` - Real Temporal runtime, use WorkflowEnvironment
- Import paths: `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))`
- Add `# noqa: E402` to imports after sys.path modification

**Common Debugging Issues:**
1. **"Workflow execution already started"** → Use unique workflow IDs (timestamp-based)
2. **"Activity not registered"** → Check activity name matches between workflow call and worker registration
3. **"RetryPolicy not found"** → Import from `temporalio.common`, not `temporalio.workflow`
4. **Integration tests fail in CI** → Use `WorkflowEnvironment`, not `Client.connect("localhost:7233")`

**Linting Fixes Applied:**
- Removed unused imports: `BeautifulSoup`, `json`, `List`, `Dict`
- Fixed line length with f-string concatenation: `f"text {var}" f"more text"`
- Fixed indentation with parentheses: `(f"line1" f"line2")`
- Used multi-line imports for long import lists
- Fixed comment spacing: `# comment` (not `#comment`)

**Dependencies:**
- Current: `temporalio`, `requests`, `beautifulsoup4`, `pytest`, `pytest-asyncio`
- Future LinkedIn agent: `openai`, `linkedin-api`, `schedule`, `pytz`

**GitHub Actions Setup:**
- Branch protection: PR required, CI must pass, linear history, no force push
- CI runs: linting, unit tests, integration tests, coverage
- Self-approval allowed for solo projects

The project is in excellent shape and ready for the next development phase! 🚀

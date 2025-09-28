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

## LinkedIn Content Creation AI Agent - Future Development

### **Phase 1: Core Content Generation Workflow** 🎯

**1. Enhanced Topic Research Activity**
- Extend the current `web_search` to focus on trending topics in your industry
- Add keyword research and competitor analysis
- Include LinkedIn-specific trending topics and hashtags

**2. Content Generation Activity**
- Create a new `generate_content` activity that uses AI to write LinkedIn posts
- Support different content types: thought leadership, industry insights, personal stories
- Include hooks, value propositions, and calls-to-action

**3. Content Optimization Activity**
- Format content for LinkedIn's algorithm (character limits, hashtags, mentions)
- Add engagement optimization (questions, polls, visual suggestions)
- Include A/B testing variations

### **Phase 2: User Experience & Workflow** 👤

**4. Interactive Content Workflow**
- Create a `LinkedInContentWorkflow` that guides users through content creation
- Add approval steps and revision cycles
- Include content preview and editing capabilities

**5. Content Management System**
- Store generated content with metadata (topics, performance, versions)
- Add content calendar and scheduling
- Include batch content generation for multiple posts

### **Phase 3: Advanced Features** 🚀

**6. LinkedIn API Integration**
- Connect to LinkedIn API for direct posting
- Add engagement tracking and analytics
- Include audience insights and performance metrics

**7. Smart Content Strategy**
- Analyze your existing content performance
- Suggest optimal posting times and content types
- Include competitor analysis and trending topic alerts

### **Phase 4: AI Enhancement** 🤖

**8. Advanced AI Features**
- Personal brand voice training
- Industry-specific content templates
- Multi-language content generation
- Visual content suggestions (images, videos, carousels)

## **Immediate Next Steps** (Recommended Implementation Order):

1. **Create a new `LinkedInContentWorkflow`** that orchestrates:
   - Topic research → Content generation → Optimization → User approval

2. **Enhance the web search** to focus on LinkedIn-relevant topics:
   - Industry trends, competitor content, trending hashtags
   - LinkedIn-specific search queries

3. **Add a content generation activity** that creates LinkedIn posts:
   - Hook + Value + Story + Call-to-action structure
   - Character count optimization (LinkedIn posts work best at 150-300 characters)
   - Hashtag suggestions

4. **Create a new starter script** for the LinkedIn content workflow

### **Technical Implementation Notes:**

**New Activities to Create:**
- `research_linkedin_topics(query: str) -> List[Dict]` - Enhanced web search for LinkedIn content
- `generate_linkedin_content(topic_data: List[Dict]) -> str` - AI content generation
- `optimize_linkedin_content(content: str) -> Dict` - Format and optimize for LinkedIn
- `schedule_linkedin_post(content: Dict) -> str` - Handle posting and scheduling

**New Workflow:**
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
        
        # Step 4: User approval (could be manual or automated)
        # Step 5: Schedule/post content
        
        return optimized
```

**Dependencies to Add:**
- `openai` or similar for AI content generation
- `linkedin-api` for LinkedIn integration
- `schedule` for content scheduling
- `pytz` for timezone handling

## Next Steps for Enhancement (Original)
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

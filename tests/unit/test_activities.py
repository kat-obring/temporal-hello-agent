import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from activities import simulate_llm_response, web_search, summarize_results  # noqa: E402


@pytest.mark.asyncio
async def test_simulate_llm_response():
    result = await simulate_llm_response("Trinity")
    assert "Trinity" in result
    assert "🤖 Agent" in result


@pytest.mark.asyncio
async def test_web_search():
    """Test the web search activity with a simple query."""
    query = "Python programming"
    results = await web_search(query)
    
    # Should return a list of results
    assert isinstance(results, list)
    assert len(results) > 0
    
    # Each result should have the required fields
    for result in results:
        assert isinstance(result, dict)
        assert "title" in result
        assert "snippet" in result
        assert "url" in result
        assert "source" in result
        assert isinstance(result["title"], str)
        assert isinstance(result["snippet"], str)
        assert isinstance(result["url"], str)
        assert isinstance(result["source"], str)


@pytest.mark.asyncio
async def test_web_search_with_empty_query():
    """Test web search with an empty query."""
    results = await web_search("")
    
    # Should still return results (fallback behavior)
    assert isinstance(results, list)
    assert len(results) > 0


@pytest.mark.asyncio
async def test_summarize_results():
    """Test the summarize_results activity with sample data."""
    query = "test query"
    search_results = [
        {
            "title": "Test Result 1",
            "snippet": "This is a test snippet for the first result.",
            "url": "https://example.com/1",
            "source": "Test Source 1"
        },
        {
            "title": "Test Result 2", 
            "snippet": "This is a test snippet for the second result.",
            "url": "https://example.com/2",
            "source": "Test Source 2"
        }
    ]
    
    args = (query, search_results)
    summary = await summarize_results(args)
    
    # Should return a string
    assert isinstance(summary, str)
    assert len(summary) > 0
    
    # Should contain the query
    assert query in summary
    
    # Should contain result titles
    assert "Test Result 1" in summary
    assert "Test Result 2" in summary
    
    # Should contain snippets
    assert "test snippet for the first result" in summary
    assert "test snippet for the second result" in summary
    
    # Should contain URLs
    assert "https://example.com/1" in summary
    assert "https://example.com/2" in summary
    
    # Should have proper formatting
    assert "🔍" in summary  # Search emoji
    assert "**" in summary  # Bold formatting
    assert "---" in summary  # Separator


@pytest.mark.asyncio
async def test_summarize_results_empty():
    """Test summarize_results with empty search results."""
    query = "test query"
    search_results = []
    
    args = (query, search_results)
    summary = await summarize_results(args)
    
    # Should return error message for empty results
    assert isinstance(summary, str)
    assert "No results found" in summary
    assert query in summary

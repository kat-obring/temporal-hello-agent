import asyncio
import requests
from temporalio import activity
from typing import List, Dict


@activity.defn
async def web_search(query: str) -> List[Dict[str, str]]:
    """Search the web for a query and return structured results."""
    print(f"🔍 Searching for: {query}")

    # For now, we'll use DuckDuckGo's instant answer API
    # In production, you might want to use Google Custom Search API or similar
    try:
        # Use DuckDuckGo's instant answer API
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract results
        results = []

        # Add abstract if available
        if data.get("Abstract"):
            results.append({
                "title": data.get("Heading", "Summary"),
                "url": data.get("AbstractURL", ""),
                "snippet": data.get("Abstract", ""),
                "source": "DuckDuckGo Abstract"
            })

        # Add related topics
        for topic in data.get("RelatedTopics", [])[:3]:  # Limit to 3 results
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({
                    "title": topic.get("Text", "")[:100] + "...",
                    "url": topic.get("FirstURL", ""),
                    "snippet": topic.get("Text", ""),
                    "source": "DuckDuckGo Related"
                })

        # If no results from DuckDuckGo, provide a fallback
        if not results:
            results.append({
                "title": f"Search results for: {query}",
                "url": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
                "snippet": (f"No instant answers found for '{query}'. "
                           f"Click to see full search results."),
                "source": "DuckDuckGo Search"
            })

        print(f"✅ Found {len(results)} search results")
        return results

    except Exception as e:
        print(f"❌ Search failed: {e}")
        # Return a fallback result
        return [{
            "title": f"Search Error for: {query}",
            "url": f"https://duckduckgo.com/?q={query.replace(' ', '+')}",
            "snippet": (f"Search encountered an error: {str(e)}. "
                        f"Please try the direct search link."),
            "source": "Error Fallback"
        }]


@activity.defn
async def summarize_results(args: tuple) -> str:
    """Summarize the search results for the user."""
    query, search_results = args
    print(f"📝 Summarizing {len(search_results)} results for: {query}")

    if not search_results:
        return (f"❌ No results found for '{query}'. "
                f"Please try a different search term.")

    # Create a structured summary
    summary_parts = [
        f"🔍 **Search Results for: {query}**",
        f"Found {len(search_results)} relevant results:\n"
    ]

    for i, result in enumerate(search_results, 1):
        summary_parts.append(f"**{i}. {result['title']}**")
        summary_parts.append(f"   {result['snippet']}")
        if result['url']:
            summary_parts.append(f"   🔗 {result['url']}")
        summary_parts.append("")  # Empty line for readability

    # Add a conclusion
    summary_parts.append("---")
    summary_parts.append(
        "💡 **Summary**: These results provide comprehensive information "
        "about your search topic. Click the links to explore further.")

    summary = "\n".join(summary_parts)
    print(f"✅ Summary completed ({len(summary)} characters)")
    return summary


# Keep the old activities for backward compatibility
@activity.defn
async def simulate_llm_response(name: str) -> str:
    await asyncio.sleep(1)  # Simulate thinking
    return f"🤖 Agent {name} says: 'Let me look that up for you...'"


@activity.defn
async def flaky_activity(name: str) -> str:
    print(f"flaky_activity called with: {name}")
    await asyncio.sleep(0.5)
    raise RuntimeError("Simulated LLM failure!")

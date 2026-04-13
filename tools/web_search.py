import os
import logging
from tavily import TavilyClient
from duckduckgo_search import DDGS
from config import MAX_SEARCH_RESULTS

logger = logging.getLogger(__name__)

# Attempt to initialize Tavily if key is available
try:
    TAVILY_KEY = os.environ.get("TAVILY_KEY", "dummy")
    tavily_client = TavilyClient(api_key=TAVILY_KEY)
except Exception as e:
    tavily_client = None
    logger.warning(f"Failed to initialize TavilyClient: {e}")

def web_search(query: str) -> str:
    """
    Search the web using Tavily. If it fails (quota, missing key, rate limit),
    transparently fallback to DuckDuckGo search.
    """
    # 1. Try Tavily
    if tavily_client and TAVILY_KEY != "dummy":
        try:
            results = tavily_client.search(query, max_results=MAX_SEARCH_RESULTS)
            formatted_results = "\n\n".join([f"Source: {r.get('url', 'Unknown')}\n{r.get('content', '')}" for r in results.get("results", [])])
            logger.info("Search fulfilled by: TAVILY")
            return f"[Web Search Results via Tavily]\n{formatted_results}"
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}. Falling back to DuckDuckGo.")
    
    # 2. Fallback to DDG
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=MAX_SEARCH_RESULTS))
            formatted_results = "\n\n".join([f"Source: {r.get('href', 'Unknown')}\n{r.get('body', '')}" for r in results])
            logger.info("Search fulfilled by: DUCKDUCKGO")
            return f"[Web Search Results via DuckDuckGo]\n{formatted_results}"
    except Exception as e:
        logger.error(f"DuckDuckGo search also failed: {e}")
        return f"[Search Error] Failed to retrieve results for: {query}"

if __name__ == "__main__":
    # Smoke test
    logging.basicConfig(level=logging.INFO)
    print("Testing search...")
    res = web_search("What is the Qwen 2.5 architecture?")
    print(res)

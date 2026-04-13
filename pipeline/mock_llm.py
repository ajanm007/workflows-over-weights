from pydantic import BaseModel
import re

class MockResponse(BaseModel):
    content: str
    tool_calls: list[str] = []

def generate_mock_response(prompt: str, stage: str) -> MockResponse:
    """
    Simulates the Qwen model. It randomly decides to use a search tool if in stage 2 or 4.
    Otherwise it outputs a standard answer block.
    """
    # Simple deterministic mocking based on text
    if "multiple choice" in prompt.lower() or "(a)" in prompt.lower():
        ans = "A"
    else:
        ans = "42"

    if (stage == "stage_2_tools" or stage == "stage_4_full") and "<SEARCH>" not in prompt:
        return MockResponse(
            content=f"Let me think about this. I should search for recent developments.\n<SEARCH>latest academic papers on this</SEARCH>",
            tool_calls=["latest academic papers on this"]
        )
    
    return MockResponse(
        content=f"Based on my analysis, the answer is apparent.\n<FINAL_ANSWER>{ans}</FINAL_ANSWER>"
    )

def extract_search_query(text: str) -> str | None:
    match = re.search(r"<SEARCH>(.*?)</SEARCH>", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_final_answer(text: str) -> str | None:
    match = re.search(r"<FINAL_ANSWER>(.*?)</FINAL_ANSWER>", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

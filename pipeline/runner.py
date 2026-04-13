import os
import json
import logging
from pathlib import Path

from config import DATASET_PATH, CHECKPOINT_PATH
from pipeline.mock_llm import generate_mock_response, extract_search_query, extract_final_answer
from pipeline.prompts import BASE_PROMPT, TOOL_AUGMENTED_PROMPT, SELF_CRITIQUE_PROMPT_SYSTEM, SELF_CRITIQUE_PROMPT_USER
from tools.web_search import web_search
from eval.scorer import score_exact_match

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_checkpoint():
    if CHECKPOINT_PATH.exists():
        try:
            with open(CHECKPOINT_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_checkpoint(data):
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump(data, f, indent=2)

def run_stage_1(item):
    """Stage 1: Zero-shot baseline without tools or critique."""
    prompt = BASE_PROMPT.format(question=item["question"])
    response = generate_mock_response(prompt, "stage_1_baseline")
    prediction = extract_final_answer(response.content) or response.content
    return {"prompt": prompt, "response": response.content, "prediction": prediction}

def run_stage_2(item):
    """Stage 2: Tool-augmented reasoning (Single Web Search)."""
    prompt = TOOL_AUGMENTED_PROMPT.format(question=item["question"])
    response = generate_mock_response(prompt, "stage_2_tools")
    
    query = extract_search_query(response.content)
    search_context = ""
    if query:
        search_results = web_search(query)
        prompt += f"\n\nModel Search Query: {query}\n{search_results}\n\nPlease continue and provide the <FINAL_ANSWER>."
        response = generate_mock_response(prompt, "stage_2_tools") # Gen again
        search_context = search_results

    prediction = extract_final_answer(response.content) or response.content
    return {"prompt": prompt, "response": response.content, "prediction": prediction, "search": query}

def run_stage_3(item, s1_content):
    """Stage 3: Self-Critique loop (No tools) based on Stage 1 answer."""
    sys_prompt = SELF_CRITIQUE_PROMPT_SYSTEM
    user_prompt = SELF_CRITIQUE_PROMPT_USER.format(question=item["question"], candidate_response=s1_content)
    combined = f"{sys_prompt}\n{user_prompt}"
    
    response = generate_mock_response(combined, "stage_3_critique")
    prediction = extract_final_answer(response.content) or response.content
    return {"prompt": combined, "response": response.content, "prediction": prediction}

def run_stage_4(item, s2_content):
    """Stage 4: Full lean pipeline (Tools + Self critique)."""
    sys_prompt = SELF_CRITIQUE_PROMPT_SYSTEM
    user_prompt = SELF_CRITIQUE_PROMPT_USER.format(question=item["question"], candidate_response=s2_content)
    combined = f"{sys_prompt}\n{user_prompt}"
    
    response = generate_mock_response(combined, "stage_4_full")
    prediction = extract_final_answer(response.content) or response.content
    return {"prompt": combined, "response": response.content, "prediction": prediction}

def run_pipeline():
    if not DATASET_PATH.exists():
        logging.error(f"Dataset missing at {DATASET_PATH}. Run fetch_data.py first.")
        return
        
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    results = load_checkpoint()
    
    # Process only local limits or full dataset
    limit = min(5, len(dataset)) # limit for mock run
    
    for idx, item in enumerate(dataset[:limit]):
        qid = str(item.get("id", idx))
        
        if qid in results:
            logging.info(f"Skipping {qid}, already in checkpoint.")
            continue
            
        logging.info(f"Processing QID: {qid} ({idx+1}/{limit})")
        expected_ans = item.get("answer", "")
        ans_type = item.get("answer_type", "exactMatch")
        
        item_results = {"expected": expected_ans, "type": ans_type, "stages": {}}
        
        s1 = run_stage_1(item)
        s1["correct"] = score_exact_match(s1["prediction"], expected_ans, ans_type)
        item_results["stages"]["1"] = s1
        
        s2 = run_stage_2(item)
        s2["correct"] = score_exact_match(s2["prediction"], expected_ans, ans_type)
        item_results["stages"]["2"] = s2
        
        s3 = run_stage_3(item, s1["response"])
        s3["correct"] = score_exact_match(s3["prediction"], expected_ans, ans_type)
        item_results["stages"]["3"] = s3
        
        s4 = run_stage_4(item, s2["response"])
        s4["correct"] = score_exact_match(s4["prediction"], expected_ans, ans_type)
        item_results["stages"]["4"] = s4
        
        results[qid] = item_results
        save_checkpoint(results)
        
    logging.info("Run complete. Checkpoint saved.")

if __name__ == "__main__":
    run_pipeline()

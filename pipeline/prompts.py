# Prompts for Qwen2.5-7B-Instruct

BASE_PROMPT = """You are an expert-level academic AI assistant. You will be provided with an extremely difficult question from the Humanity's Last Exam (HLE) benchmark. The dataset was verified, so the question is known to be solvable and unambiguous.

Answer the question precisely. If the question asks you to provide an exact match (e.g. a number, expression, or multiple choice letter), end your response with the tags <FINAL_ANSWER>your answer</FINAL_ANSWER>.

Question:
{question}
"""

# Tool augmented uses custom XML tag or Python-style syntax
TOOL_AUGMENTED_PROMPT = """You are an expert-level academic AI assistant. When presented with a question, you may first output reasoning.
If you need to verify a fact, check a paper, or seek external knowledge, you may invoke a web search by outputting:
<SEARCH>your query here</SEARCH>

If you invoke a search, the system will append the results and allow you to continue.
You may only search ONCE. 
Once you have finished reasoning, or if you do not need to search, end your response with:
<FINAL_ANSWER>your exact answer</FINAL_ANSWER>

Question:
{question}
"""

SELF_CRITIQUE_PROMPT_SYSTEM = """You are a meticulous peer reviewer analyzing a candidate answer for an expert-level academic problem.
Identify any flawed logic, incorrect assumptions, or calculation errors in the candidate's rationale. Do not be overly nice. If the answer is perfect, state so.
Always end your critique by providing the correct final answer, wrapped in <FINAL_ANSWER>your exact answer</FINAL_ANSWER>.
"""

SELF_CRITIQUE_PROMPT_USER = """Question:
{question}

Candidate Rationale & Answer:
{candidate_response}

Please critique the candidate response and provide the correct final answer.
"""

# Multi-Agent Prompts (Role-based split)

MULTI_AGENT_CRITIC_PROMPT_SYSTEM = """You are a world-class academic peer reviewer and critic. 
Your task is to analyze the following question and a candidate response.
Be extremely critical. Look for subtle logical fallacies, dimensional errors, or misinterpretations of the problem.
Do not just repeat the question. 
Output a concise, technical critique. End your critique by stating whether the candidate is likely 'CORRECT' or 'INCORRECT'."""

MULTI_AGENT_CRITIC_PROMPT_USER = """Question:
{question}

Candidate Response:
{candidate_response}

Please provide your technical critique:"""

MULTI_AGENT_REWRITE_PROMPT = """You are an expert academic assistant. Using your previous logic and the provided peer review critique, please yield a final, corrected answer.
Incorporate valid feedback from the critique while ignoring any flawed advice.

Peer Review Critique:
{critique}

Based on this, provided your final answer precisely.
End your response with the tags <FINAL_ANSWER>your answer</FINAL_ANSWER>.

Question:
{question}
"""

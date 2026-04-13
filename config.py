import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
EVAL_DIR = BASE_DIR / "eval"
PROMPTS_DIR = BASE_DIR / "prompts" / "v1"
PIPELINE_DIR = BASE_DIR / "pipeline"

# Data paths
DATASET_PATH = DATA_DIR / "hle_verified_gold.json"
CHECKPOINT_PATH = DATA_DIR / "checkpoint.json"

# Search configurations
MAX_SEARCHES_PER_QUESTION = 1
MAX_SEARCH_RESULTS = 3

# Model constraints mock
MAX_TOKENS = 4096

# Stages
STAGES = [
    "stage_1_baseline",
    "stage_2_tools",
    "stage_3_critique",
    "stage_4_full"
]

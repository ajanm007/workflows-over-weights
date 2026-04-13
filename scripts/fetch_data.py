import os
import json
import logging
from datasets import load_dataset

from config import DATASET_PATH, DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_and_filter_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    logging.info("Downloading skylenage/HLE-Verified dataset from HuggingFace...")
    # The dataset has subsets? Let's just load 'default' or see if we need to configure it.
    # From PRD and metadata, it's a single split or multiple splits, but "Verified_Classes" column distinguishes.
    try:
        ds = load_dataset("skylenage/HLE-Verified", split="train")
    except Exception as e:
        logging.error(f"Failed to load dataset: {e}")
        return
    
    logging.info(f"Loaded {len(ds)} total items.")
    
    gold_text_items = []
    
    for item in ds:
        # Filter for Gold subset
        if item.get("Verified_Classes") != "Gold subset":
            continue
            
        # Filter for text-only (image and image_preview should be null or empty strings)
        img = item.get("image")
        img_prev = item.get("image_preview")
        rat_img = item.get("rationale_image")
        
        # We consider text-only if all image fields are logically empty
        has_img = img and str(img).strip() != "null" and str(img).strip() != ""
        has_prev = img_prev and str(img_prev).strip() != "null" and str(img_prev).strip() != ""
        has_rat = rat_img and str(rat_img).strip() != "null" and str(rat_img).strip() != ""
        
        if has_img or has_prev or has_rat:
            continue
            
        gold_text_items.append(item)
    
    logging.info(f"Filtered to {len(gold_text_items)} Gold text-only items.")
    
    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(gold_text_items, f, indent=2, ensure_ascii=False)
        
    logging.info(f"Saved dataset to {DATASET_PATH}")
    
if __name__ == "__main__":
    fetch_and_filter_data()

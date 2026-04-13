import string
import re

def normalize_text(text: str) -> str:
    """
    Lowercase, strip whitespaces, and basic punctuation removal for robust exact matching.
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.lower().strip()
    # Remove standard punctuation but keep math-relevant chars like - / .
    text = text.translate(str.maketrans("", "", string.punctuation.replace("-", "").replace("/", "").replace(".", "")))
    return " ".join(text.split())

def check_numerical_equivalence(prediction: str, reference: str) -> bool:
    """
    Basic numerical equivalence (e.g., handles 1/2 vs 0.5 if they arrive cleanly).
    """
    try:
        if "/" in prediction:
            p_parts = prediction.split("/")
            p_val = float(p_parts[0]) / float(p_parts[1])
        else:
            p_val = float(prediction)
            
        if "/" in reference:
            r_parts = reference.split("/")
            r_val = float(r_parts[0]) / float(r_parts[1])
        else:
            r_val = float(reference)
            
        return abs(p_val - r_val) < 1e-5
    except ValueError:
        return False
    except ZeroDivisionError:
        return False

def score_exact_match(prediction: str, expected_answer: str, answer_type: str = "exactMatch") -> bool:
    """
    Evaluates if the prediction exactly matches the expected answer, accounting for basic numeric equivalence.
    """
    norm_pred = normalize_text(prediction)
    norm_exp = normalize_text(expected_answer)
    
    # 1. Direct string match after normalization
    if norm_pred == norm_exp:
        return True
    
    # 2. Check if the prediction cleanly ends with or contains the exact expected answer as a discrete token
    tokens = norm_pred.split()
    if norm_exp in tokens:
        return True
        
    # 3. Handle multiple choice formats where prediction might be "(A)" but expected is "A"
    if answer_type == "multipleChoice":
        if len(norm_exp) == 1 and norm_exp.isalpha():
            if f"({norm_exp})" in prediction.lower() or f"{norm_exp})" in prediction.lower():
                return True
                
    # 4. Attempt numerical evaluation for purely mathematical discrepancies
    if check_numerical_equivalence(norm_pred.replace(" ", ""), norm_exp.replace(" ", "")):
        return True
        
    return False

if __name__ == "__main__":
    # Quick tests
    assert score_exact_match("1/2", "0.5") == True
    assert score_exact_match("D", "D", "multipleChoice") == True
    assert score_exact_match("the answer is 42.", "42", "exactMatch") == True
    assert score_exact_match("10.5", "10.05") == False
    print("Scorer unit tests passed.")

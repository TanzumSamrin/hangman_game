import json
import random

DIFFICULTY_SETTINGS = {
    "easy": {"max_attempts": 8},
    "medium": {"max_attempts": 6},
    "hard": {"max_attempts": 4}
}

def load_random_word(difficulty="medium", category=None):
    with open("words.json", "r") as file:
        data = json.load(file)
    
    diff_data = data.get(difficulty.lower(), data["medium"])
    
    if category and category in diff_data:
        word_list = diff_data[category]
    else:
        # Pick from all categories within selected difficulty
        word_list = [word for cat in diff_data.values() for word in cat]
        
    return random.choice(word_list).lower()
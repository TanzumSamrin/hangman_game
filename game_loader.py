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
    
    # Filter by specific category if selected
    if category and category.lower() in diff_data:
        word_list = diff_data[category.lower()]
    else:
        # Combine all categories under the chosen difficulty
        word_list = [word for cat in diff_data.values() for word in cat]
        
    return random.choice(word_list).lower()
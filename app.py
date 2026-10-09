from flask import Flask, render_template, request, jsonify, session
from game_loader import load_random_word, DIFFICULTY_SETTINGS
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start_game():
    data = request.json or {}
    difficulty = data.get("difficulty", "medium")
    category = data.get("category", None)  # Reads selected category from UI
    
    session["word"] = load_random_word(difficulty, category)
    session["max_attempts"] = DIFFICULTY_SETTINGS.get(difficulty, {}).get("max_attempts", 6)
    session["guessed"] = []
    session["incorrect"] = 0

    return jsonify(get_game_state())

@app.route("/api/guess", methods=["POST"])
def make_guess():
    letter = request.json.get("letter", "").lower()
    
    if not letter or letter in session["guessed"]:
        return jsonify(get_game_state())

    session["guessed"].append(letter)
    if letter not in session["word"]:
        session["incorrect"] += 1

    session.modified = True
    return jsonify(get_game_state())

def get_game_state():
    word = session.get("word", "")
    guessed = session.get("guessed", [])
    max_attempts = session.get("max_attempts", 6)
    incorrect = session.get("incorrect", 0)

    display = [l if l in guessed else "_" for l in word]
    won = "_" not in display and len(word) > 0
    lost = incorrect >= max_attempts

    return {
        "display": " ".join(display),
        "guessed": guessed,
        "attempts_left": max_attempts - incorrect,
        "status": "won" if won else ("lost" if lost else "playing"),
        "word": word if (won or lost) else None
    }

if __name__ == "__main__":
    app.run(debug=True)
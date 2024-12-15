import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, request
from src.chatbot import load_intents, preprocess_input, match_intent, get_response
from src.exercise import breathing_exercise

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Load intents
intents = load_intents("/Users/paniztafreshi/PanicAttackBot/data/intents.json")

@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["message"]
    print(f"Received input: {user_input}")  # Debug print
    # Process the input
    user_input = preprocess_input(user_input)
    intent = match_intent(user_input, intents)

    if intent:
        if intent["tag"] == "breathing_exercise":
            return "Let's start a breathing exercise together! Inhale for 4 seconds, hold for 7 seconds, and exhale for 8 seconds."
        else:
            return get_response(intent)
    else:
        return "Sorry, I didn't understand that."
    
if __name__ == "__main__":
    app.run()

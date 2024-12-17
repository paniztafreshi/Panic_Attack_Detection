import sys
import os
from google.cloud import storage  # Import Google Cloud Storage client
from flask import Flask, render_template, request
from src.chatbot import load_intents, preprocess_input, match_intent, get_response
from src.exercise import breathing_exercise

# Set Google Application Credentials for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-cloud-key.json"
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Function to download dataset from Google Cloud Storage
def download_dataset(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the Google Cloud Storage bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Downloaded {source_blob_name} to {destination_file_name}.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        raise

# Google Cloud Storage configuration
bucket_name = "mentalhealth-dataset"  
source_blob_name = "intents.json" 
destination_file_name = "data/intents.json"  

# Ensure the data directory exists
os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)

# Download the intents.json file from Google Cloud Storage
try:
    download_dataset(bucket_name, source_blob_name, destination_file_name)
except Exception as e:
    print("Failed to download dataset. Ensure Google Cloud credentials and bucket configuration are correct.")
    sys.exit(1)

# Load intents
try:
    intents = load_intents(destination_file_name)
    print("Successfully loaded intents.")
except Exception as e:
    print(f"Failed to load intents: {e}")
    sys.exit(1)

@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    try:
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
    except Exception as e:
        print(f"Error processing user input: {e}")
        return "Sorry, there was an error processing your request."

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))  
    app.run(host="0.0.0.0", port=port, debug='True')

from flask import Flask, jsonify, request
import logging
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
jwt = JWTManager(app)

logging.basicConfig(level=logging.INFO)

class PredictionSchema(Schema):
    text = fields.Str(required=True)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Chatbot that might help!"})

@cache.cached(timeout=60)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = PredictionSchema().load(request.get_json())
        user_input = data['text']
        # Dummy prediction logic
        prediction = "positive" if "happy" in user_input else "negative"
        return jsonify({"prediction": prediction})
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)


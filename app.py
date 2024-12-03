from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.model import MemeRecommendationModel

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the meme recommendation model
meme_model = MemeRecommendationModel()


@app.route('/recommend_meme', methods=['POST'])
def recommend_meme():
    """
    Endpoint to get meme recommendations based on conversation context
    """
    try:
        # Get conversation from request
        data = request.json
        conversation = data.get('conversation', '')

        if not conversation:
            return jsonify({
                'error': 'No conversation provided',
                'status': 400
            }), 400

        # Get meme recommendations
        recommended_memes = meme_model.recommend_memes(conversation)

        return jsonify({
            'recommended_memes': recommended_memes,
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 500
        }), 500


@app.route('/train_model', methods=['POST'])
def train_model():
    """
    Endpoint to retrain or update the meme recommendation model
    """
    try:
        # Trigger model retraining
        meme_model.train()

        return jsonify({
            'message': 'Model successfully retrained',
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 500
        }), 500


if __name__ == '__main__':
    # Ensure necessary directories exist
    os.makedirs('meme_database', exist_ok=True)
    os.makedirs('model_checkpoints', exist_ok=True)

    # Run the Flask app
    app.run(debug=True, port=5000)
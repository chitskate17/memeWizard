from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key="AIzaSyC9vQK42erx2idQ6HjLVkh0_aDX3VNiIbs")

# MongoDB connection string
MONGO_URI = "mongodb+srv://chiragprao2004:FHhfSh9LRY5xCWLt@cluster0.668wx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['SentimentDB']
collection = db['SentimentCollection']


# Routes

@app.route('/')
def landing_page():
    """Landing page route"""
    return render_template('landing.html')


@app.route('/recommender.html')
def meme_recommender():
    """Recommender page route"""
    return render_template('recommender.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate meme recommendations"""
    try:
        input_text = request.form.get('input_text')
        if not input_text:
            return jsonify({'error': 'Input text is required.'}), 400

        # Sentiment classification
        sentiments = ai_generator(input_text)

        # Fetch and rank Image_URLs based on sentiments
        image_urls = fetch_ranked_image_urls(sentiments)

        return jsonify({'sentiments': sentiments, 'image_urls': image_urls})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Helper Functions

def ai_generator(input_text):
    """Generates sentiment classifications using Google Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(
            f"""classify the below text into Joyful,Sad,Angry,Fearful,Surprised,Disgusted,Confident,Nostalgic,
            Sarcastic,Excited,Bored,Anxious,Content,Motivated,Romantic,Frustrated,Jealous,Grateful,Curious,Embarrassed 
            if there are multiple also add it, just only respond with the classified keyword and nothing else or else the app will crash 
            {input_text}"""
        )
        classified_sentiments = response.text.strip()
        return classified_sentiments.split(",")  # Split multiple sentiments into a list
    except Exception as e:
        raise RuntimeError(f"AI generator error: {str(e)}")


def fetch_ranked_image_urls(input_sentiments):
    """Fetches and ranks image URLs from the database based on sentiment matches."""
    try:
        input_sentiments = [sentiment.strip().lower() for sentiment in input_sentiments]
        results = collection.find({}, {"Image_URL": 1, "Sentimental": 1, "_id": 0})

        ranked_results = []
        for result in results:
            sentimental_value = result.get("Sentimental", "")
            if not isinstance(sentimental_value, str):
                continue  # Skip documents where Sentimental is not a string

            doc_sentiments = [s.strip().lower() for s in sentimental_value.split(",")]
            match_count = len(set(input_sentiments) & set(doc_sentiments))
            if match_count > 0:
                ranked_results.append({"Image_URL": result.get("Image_URL"), "match_count": match_count})

        ranked_results.sort(key=lambda x: x["match_count"], reverse=True)
        top_results = ranked_results[:5]

        return [result['Image_URL'] for result in top_results]
    except Exception as e:
        raise RuntimeError(f"Database query error: {str(e)}")


# Main entry point
if __name__ == '__main__':
    app.run(debug=True)

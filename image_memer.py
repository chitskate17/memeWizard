import httpx
import base64
import google.generativeai as genai
from pymongo import MongoClient
from PIL import Image
import pytesseract

# Configure Google Generative AI
genai.configure(api_key="AIzaSyC9vQK42erx2idQ6HjLVkh0_aDX3VNiIbs")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# MongoDB connection string
MONGO_URI = "mongodb+srv://123gamein:123gamein@memer.tcml6.mongodb.net/?retryWrites=true&w=majority&appName=Memer"

# Define the database and collection names
db_name = "SentimentDB"
collection_name = "SentimentCollection"


# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None


# Function to classify sentiments using Generative AI
def classify_sentiments(conversation_text):
    prompt = (
        "Classify the below text into Joyful, Sad, Angry, Fearful, Surprised, Disgusted, "
        "Confident, Nostalgic, Sarcastic, Excited, Bored, Anxious, Content, Motivated, "
        "Romantic, Frustrated, Jealous, Grateful, Curious, Embarrassed. If there are multiple "
        "sentiments, include them all. Only respond with the classified keywords as a comma-separated list."
    )
    # Call the Gemini API
    response = model.generate_content(f"{conversation_text}\n\n{prompt}")

    # Check the structure of `response`
    print("Response object:", response)

    # Extract the text attribute (assume it is called `text`, update if different)
    if hasattr(response, 'text'):
        sentiments = response.text.strip()  # Use the correct attribute
    else:
        raise ValueError("Unexpected response format from Gemini API.")

    # Split sentiments into a list
    return [s.strip() for s in sentiments.split(",")]


# Function to fetch and rank Image_URLs based on sentiment match
def fetch_ranked_image_urls(input_sentiments):
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[db_name]
    collection = db[collection_name]

    input_sentiments = [sentiment.lower() for sentiment in input_sentiments]

    results = collection.find({}, {"Image_URL": 1, "Sentimental": 1, "_id": 0})

    ranked_results = []
    for result in results:
        sentimental_value = result.get("Sentimental", "")
        if not isinstance(sentimental_value, str):
            continue

        doc_sentiments = [s.strip().lower() for s in sentimental_value.split(",")]
        match_count = len(set(input_sentiments) & set(doc_sentiments))
        if match_count > 0:
            ranked_results.append({"Image_URL": result.get("Image_URL"), "match_count": match_count})

    ranked_results.sort(key=lambda x: x["match_count"], reverse=True)
    top_results = ranked_results[:5]

    if top_results:
        print("\nTop 5 Image_URLs based on sentiment match:")
        for idx, result in enumerate(top_results, start=1):
            print(f"{idx}. {result['Image_URL']} (Matches: {result['match_count']})")
    else:
        print("No Image_URLs matched the given sentiments.")

    # Close the MongoDB connection
    client.close()


# Main function to integrate OCR and sentiment classification
def main():
    # Image path for OCR
    image_path = "convo2.png"  # Replace with your image path

    # Step 1: Extract text using Tesseract OCR
    print("Extracting text from image using OCR...")
    conversation_text = extract_text_from_image(image_path)
    if not conversation_text:
        print("No text extracted from the image. Exiting.")
        return

    print(f"Extracted Text: {conversation_text}")

    # Step 2: Classify sentiments using Generative AI
    print("\nClassifying sentiments...")
    classified_sentiments = classify_sentiments(conversation_text)
    print(f"Classified Sentiments: {classified_sentiments}")

    # Step 3: Fetch and rank Image_URLs based on classified sentiments
    print("\nFetching and ranking Image_URLs...")
    fetch_ranked_image_urls(classified_sentiments)


# Run the main function
if __name__ == "__main__":
    main()

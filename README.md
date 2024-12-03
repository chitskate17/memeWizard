# memeWizard
Meme Recommendation Model that prompts relevant memes based on the contextual analysis of a conversation happening in a chat messenger
# Meme Recommendation System using Sentiment Analysis

This project develops a meme recommendation system that leverages sentiment analysis to suggest memes based on user conversations.  The system uses the VADER sentiment analysis model to classify conversation text and recommends relevant memes from a dataset.

## Table of Contents

* [Project Structure](#project-structure)
* [Technologies Used](#technologies-used)
* [Setup Instructions](#setup-instructions)
* [Data Structure](#data-structure)
* [Sentiment Classification](#sentiment-classification)
* [Meme Recommendation Logic](#meme-recommendation-logic)
* [Best Practices](#best-practices)
* [Contributing](#contributing)
* [License](#license)


## Project Structure

meme-recommendation/
data/
memes_dataset.csv - Dataset containing memes and their sentiments.


src/
main.py - Main script for running the application.


sentiment_analysis.py - Module for performing sentiment analysis.


meme_recommender.py - Module for recommending memes based on sentiment.


utils.py - Utility functions.


requirements.txt - Python dependencies.


README.md - Project documentation.

## Technologies Used

* Python 3.x
* Pandas (for data manipulation)
* NLTK / VADER Sentiment (for sentiment analysis)
* NumPy (for numerical operations)


## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/chitskate17/memeWizard>
   cd meme-recommendation

2. **Install Dependencies:**

Create a virtual environment and install the required packages:

```python -m venv venv


`source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

`pip install -r requirements.txt`

Prepare the Dataset:

Ensure that your meme dataset (memes_dataset.csv) is placed in the data/ directory. The dataset should contain the following columns:

meme_explanation: A description of the meme.

image_url: URL of the meme image.

meme_image: (Optional) The meme image itself (consider storage solutions like cloud storage for larger files).

sentiment: The sentiment category of the meme (e.g., "Joyful", "Sad", "Angry").

Data Structure

The memes_dataset.csv file should be a CSV file with at least the columns specified above. Example row:

meme_explanation,image_url,sentiment
"Drakeposting meme",https://example.com/drakeposting.jpg,Joyful
"Distracted Boyfriend meme",https://example.com/boyfriend.jpg,Sad

Sentiment Classification

The system uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis model to classify conversation text into various emotional categories. These categories include (but are not limited to):

Joyful, Sad, Angry, Fearful, Surprised, Disgusted, Confident, Nostalgic, Sarcastic, Excited, Bored, Anxious, Content, Motivated, Romantic, Frustrated, Jealous, Grateful, Curious, Embarrassed

Meme Recommendation Logic

Input: User conversation text.

Process:

Classify the text using VADER to determine its sentiment by making a gemini API call.

Map the classified sentiment to corresponding meme prompts stored in the dataset.

Filter the dataset for memes with the matching sentiment.

Return a list of recommended memes (e.g., URLs of meme images).

URLs of meme images is converted to an image.

Output: A list of recommended memes based on the detected sentiment.


License

[MIT License]

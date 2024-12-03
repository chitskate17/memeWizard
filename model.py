import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import random


class MemeRecommendationModel:
    def __init__(self,
                 embedding_model='all-MiniLM-L6-v2',
                 meme_database_path='meme_database/memes.json'):
        """
        Initialize the meme recommendation model

        :param embedding_model: Sentence transformer model for embeddings
        :param meme_database_path: Path to meme database JSON
        """
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)

        # Meme database path
        self.meme_database_path = meme_database_path

        # Load or initialize meme database
        self.meme_database = self._load_meme_database()

        # Precompute meme embeddings
        self.meme_embeddings = self._compute_meme_embeddings()

    def _load_meme_database(self):
        """
        Load or create meme database

        :return: Dictionary of memes
        """
        if not os.path.exists(self.meme_database_path):
            # If no database exists, initialize with some default memes
            default_memes = self._fetch_default_memes()

            # Ensure directory exists
            os.makedirs(os.path.dirname(self.meme_database_path), exist_ok=True)

            # Save default memes
            with open(self.meme_database_path, 'w') as f:
                json.dump(default_memes, f)

            return default_memes

        # Load existing database
        with open(self.meme_database_path, 'r') as f:
            return json.load(f)

    def _fetch_default_memes(self, num_memes=100):
        """
        Fetch default memes from an online source

        :param num_memes: Number of memes to fetch
        :return: List of meme dictionaries
        """
        # Example using Reddit's r/memes
        try:
            response = requests.get(
                f'https://www.reddit.com/r/memes/top.json?limit={num_memes}',
                headers={'User-agent': 'meme_bot 0.1'}
            )
            data = response.json()

            # Extract meme URLs
            memes = []
            for post in data['data']['children']:
                if 'preview' in post['data']:
                    meme_url = post['data']['preview']['images'][0]['source']['url']
                    meme_title = post['data']['title']

                    memes.append({
                        'url': meme_url,
                        'title': meme_title,
                        'context_keywords': self._extract_keywords(meme_title)
                    })

            return memes
        except Exception:
            # Fallback to minimal meme set
            return [
                {
                    'url': 'https://i.imgflip.com/1bij.jpg',
                    'title': 'Default Meme',
                    'context_keywords': ['funny', 'humor', 'meme']
                }
            ]

    def _extract_keywords(self, text):
        """
        Extract key keywords from text

        :param text: Input text
        :return: List of keywords
        """
        # Simple keyword extraction
        import re
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())

        # Remove common stop words
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'])

        # Split and filter keywords
        keywords = [
            word for word in text.split()
            if word not in stop_words and len(word) > 2
        ]

        return keywords[:5]  # Limit to top 5 keywords

    def _compute_meme_embeddings(self):
        """
        Precompute embeddings for memes in the database

        :return: Numpy array of meme embeddings
        """
        # Extract context keywords for embedding
        context_texts = [
            ' '.join(meme.get('context_keywords', []))
            for meme in self.meme_database
        ]

        # Generate embeddings
        return self.embedding_model.encode(context_texts)

    def recommend_memes(self, conversation, top_k=5):
        """
        Recommend memes based on conversation context

        :param conversation: Input conversation text
        :param top_k: Number of memes to recommend
        :return: List of recommended meme URLs
        """
        # Embed conversation
        conversation_embedding = self.embedding_model.encode([conversation])[0]

        # Compute similarities
        similarities = cosine_similarity(
            [conversation_embedding],
            self.meme_embeddings
        )[0]

        # Get top-k indices
        top_indices = similarities.argsort()[-top_k:][::-1]

        # Collect recommended memes
        recommended_memes = [
            self.meme_database[idx]['url']
            for idx in top_indices
        ]

        return recommended_memes

    def train(self, new_memes=None):
        """
        Train/update the meme recommendation model

        :param new_memes: Optional list of new memes to add
        """
        if new_memes:
            # Add new memes to database
            self.meme_database.extend(new_memes)

            # Save updated database
            with open(self.meme_database_path, 'w') as f:
                json.dump(self.meme_database, f)

        # Recompute embeddings
        self.meme_embeddings = self._compute_meme_embeddings()

        print(f"Model updated with {len(self.meme_database)} memes")


if __name__ == '__main__':
    # Example usage
    model = MemeRecommendationModel()

    # Test recommendation
    conversation = "I'm feeling stressed about work"
    recommended_memes = model.recommend_memes(conversation)

    print("Recommended Memes:")
    for meme in recommended_memes:
        print(meme)
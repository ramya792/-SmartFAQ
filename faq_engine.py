"""
faq_engine.py
FAQ Matching Engine for SmartFAQ.
Loads FAQ dataset, computes TF-IDF representations, and measures cosine
similarity to find the best-matching answer for user questions.
"""

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_text

# Default polite fallback response for low similarity or unanswerable queries
DEFAULT_FALLBACK = (
    "Sorry, I could not find a suitable answer to your question. "
    "Please try asking in a different way or contact the college office for more information."
)


def load_faqs(filepath: str = "faq_data.json") -> list:
    """
    Safely load FAQ data from a local JSON file.

    Args:
        filepath (str): Path to the JSON file containing FAQ data.

    Returns:
        list: List of dictionaries with 'question' and 'answer' keys.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        # Handle file read or JSON parse errors safely without crashing
        return []


def get_best_answer(user_question: str, faqs: list, threshold: float = 0.20) -> dict:
    """
    Find the best matching FAQ answer for a given user question using TF-IDF and Cosine Similarity.

    Workflow:
    1. Preprocess user question and all stored FAQ questions.
    2. Transform preprocessed texts using Scikit-learn's TfidfVectorizer.
    3. Compute Cosine Similarity between user question vector and FAQ vectors.
    4. Return highest-scoring answer if above similarity threshold, else return fallback.

    Args:
        user_question (str): The question asked by the user.
        faqs (list): List of FAQ dictionaries.
        threshold (float): Minimum similarity score required to accept a match (default: 0.20).

    Returns:
        dict: {
            "answer": str,
            "score": float,
            "matched_question": str or None,
            "is_fallback": bool
        }
    """
    # 1. Edge Case: Empty input or missing FAQ list
    if not user_question or not faqs:
        return {
            "answer": DEFAULT_FALLBACK,
            "score": 0.0,
            "matched_question": None,
            "is_fallback": True,
        }

    # 2. Preprocess user input
    cleaned_user_q = preprocess_text(user_question)
    if not cleaned_user_q.strip():
        return {
            "answer": DEFAULT_FALLBACK,
            "score": 0.0,
            "matched_question": None,
            "is_fallback": True,
        }

    # 2b. Handle common greetings
    greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "hi there", "hello there"]
    if cleaned_user_q.strip().lower() in greetings:
        return {
            "answer": "Hello! 👋 I'm your College FAQ Assistant. How can I help you with your college queries today?",
            "score": 1.0,
            "matched_question": "Greeting",
            "is_fallback": False,
        }

    # 3. Extract and preprocess all FAQ questions
    faq_questions = [faq.get("question", "") for faq in faqs]
    cleaned_faqs = [preprocess_text(q) for q in faq_questions]

    # Validate that preprocessed corpus is non-empty
    if not any(cleaned_faqs):
        return {
            "answer": DEFAULT_FALLBACK,
            "score": 0.0,
            "matched_question": None,
            "is_fallback": True,
        }

    try:
        # 4. Construct corpus and calculate TF-IDF vectors
        corpus = cleaned_faqs + [cleaned_user_q]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Separate FAQ vectors (all except last) and User vector (last row)
        faq_vectors = tfidf_matrix[:-1]
        user_vector = tfidf_matrix[-1]

        # 5. Compute Cosine Similarity
        similarities = cosine_similarity(user_vector, faq_vectors).flatten()

        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])

        # 6. Apply Similarity Threshold
        if best_score >= threshold:
            matched_faq = faqs[best_index]
            return {
                "answer": matched_faq.get("answer", DEFAULT_FALLBACK),
                "score": best_score,
                "matched_question": matched_faq.get("question", None),
                "is_fallback": False,
            }
        else:
            return {
                "answer": DEFAULT_FALLBACK,
                "score": best_score,
                "matched_question": None,
                "is_fallback": True,
            }

    except Exception:
        # Catch any mathematical or vectorization edge cases gracefully
        return {
            "answer": DEFAULT_FALLBACK,
            "score": 0.0,
            "matched_question": None,
            "is_fallback": True,
        }

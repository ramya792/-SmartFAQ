"""
nlp_utils.py
Natural Language Processing utility module for SmartFAQ.
Handles NLTK resource management and text preprocessing: lowercasing,
punctuation removal, tokenization, stopword removal, and lemmatization.
"""

import string

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    nltk = None

# List of essential NLTK data resources
NLTK_RESOURCES = ["stopwords", "wordnet", "omw-1.4", "punkt", "punkt_tab"]


def ensure_nltk_resources():
    """
    Automatically download required NLTK datasets quietly if they are missing.
    Prevents runtime crashes on machines where NLTK data isn't pre-downloaded.
    """
    if not NLTK_AVAILABLE:
        return
    for resource in NLTK_RESOURCES:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            # Fallback quietly if network download is blocked or unavailable
            pass


# Run download check upon module import
ensure_nltk_resources()

# Lazy loading of NLTK tools to handle missing resources gracefully
try:
    if NLTK_AVAILABLE:
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import WordNetLemmatizer

        ENGLISH_STOPWORDS = set(stopwords.words("english"))
        LEMMATIZER = WordNetLemmatizer()
    else:
        ENGLISH_STOPWORDS = set()
        LEMMATIZER = None
except Exception:
    ENGLISH_STOPWORDS = set()
    LEMMATIZER = None


def preprocess_text(text: str) -> str:
    """
    Preprocess user questions and FAQ text for feature extraction.

    Steps:
    1. Handle empty/invalid input safely.
    2. Convert text to lowercase.
    3. Remove punctuation marks.
    4. Tokenize into individual words.
    5. Filter out common English stopwords.
    6. Apply WordNet lemmatization to normalize words to base forms.

    Returns:
        str: Space-separated string of processed tokens.
    """
    # 1. Handle empty or non-string input safely
    if not text or not isinstance(text, str):
        return ""

    # 2. Convert text to lowercase
    text = text.lower()

    # 3. Remove punctuation using translation table
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 4. Tokenize text into words
    try:
        from nltk.tokenize import word_tokenize

        tokens = word_tokenize(text)
    except Exception:
        # Fallback to simple whitespace splitting if NLTK tokenizer is unavailable
        tokens = text.split()

    # 5. Remove English stopwords & non-alphanumeric tokens
    filtered_tokens = []
    for token in tokens:
        if token and token not in ENGLISH_STOPWORDS and token.isalnum():
            filtered_tokens.append(token)

    # 6. Apply lemmatization to reduce words to their root forms
    if LEMMATIZER:
        lemmatized_tokens = []
        for token in filtered_tokens:
            try:
                lemmatized_tokens.append(LEMMATIZER.lemmatize(token))
            except Exception:
                lemmatized_tokens.append(token)
        filtered_tokens = lemmatized_tokens

    # Return space-separated clean string
    return " ".join(filtered_tokens)

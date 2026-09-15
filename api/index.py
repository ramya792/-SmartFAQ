"""
api/index.py
FastAPI Serverless Backend for SmartFAQ on Vercel.
"""

import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Add project root directory to sys.path for module resolution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from faq_engine import load_faqs, get_best_answer

# Initialize FastAPI application (exposed as top-level variable `app`)
app = FastAPI(
    title="SmartFAQ API",
    description="College FAQ Assistant API powered by local NLP TF-IDF & Cosine Similarity",
    version="1.0.0",
)

# Enable CORS for frontend interactions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAQ dataset at startup
FAQ_PATH = os.path.join(ROOT_DIR, "faq_data.json")
FAQS = load_faqs(FAQ_PATH)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    matched_question: Optional[str] = None
    confidence: float


@app.get("/api")
def get_status():
    """Health check / status endpoint."""
    return {
        "status": "online",
        "message": "SmartFAQ API is running successfully.",
        "faqs_loaded": len(FAQS),
    }


@app.post("/api/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    """
    Process a user's question and return the best matching FAQ answer.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question string cannot be empty.")

    # Refresh FAQs if empty (e.g. hot reload or deferred load)
    faqs_to_use = FAQS if FAQS else load_faqs(FAQ_PATH)

    result = get_best_answer(request.question.strip(), faqs_to_use, threshold=0.20)

    # Format response as expected by frontend
    confidence_score = round(float(result.get("score", 0.0)), 4)
    matched_q = result.get("matched_question")

    return QuestionResponse(
        answer=result.get("answer", "Sorry, I could not process your question."),
        matched_question=matched_q if matched_q else None,
        confidence=confidence_score,
    )

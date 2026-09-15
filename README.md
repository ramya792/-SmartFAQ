# SmartFAQ – College FAQ Assistant

**Full-Stack Vercel-Compatible Web Application**

SmartFAQ is a complete, beginner-friendly, professional, and lightweight **College FAQ Assistant** built with Python (FastAPI), HTML5/CSS3/JavaScript, NLTK, and Scikit-learn. It assists students, applicants, and parents by retrieving instant, accurate answers to common college queries regarding admissions, courses, fees, examinations, hostel facilities, placements, and campus services.

---

## 📌 Project Overview

SmartFAQ allows users to ask questions in plain English. The application processes user queries using Natural Language Processing (NLP), computes numerical text representations with **TF-IDF Vectorization**, and evaluates **Cosine Similarity** against a structured local dataset (`faq_data.json`) to return the most relevant answer without relying on any external AI API or paid internet service.

---

## 🎯 Key Features

- **100% Local & Free:** Runs completely offline without API keys, external LLM calls, or paid database dependencies.
- **Vercel-Ready Architecture:** Clean full-stack separation with a serverless FastAPI backend (`/api/ask`) and static frontend (`/public/index.html`).
- **Natural Language Preprocessing:** Uses NLTK for lowercasing, punctuation stripping, tokenization, stopword filtering, and WordNet lemmatization.
- **TF-IDF & Cosine Similarity Matching:** Computes vector similarity with a similarity threshold (`0.20`) to deliver accurate answers or polite fallback messages.
- **Clean Responsive UI:** Designed with modern typography, subtle blue/navy accents, suggested question chips, loading indicators, and full mobile responsiveness.
- **Safe & Modifiable Dataset:** Easily replace or extend `faq_data.json` with verified institution-specific FAQs.

---

## 🛠️ Technologies Used

- **Python & FastAPI:** High-performance web framework for the backend API.
- **HTML5, CSS3, JavaScript (Vanilla):** Light, responsive frontend UI.
- **NLTK (Natural Language Toolkit):** Text preprocessing (tokenization, stopwords, lemmatization).
- **Scikit-learn:** TF-IDF vectorization (`TfidfVectorizer`) and cosine similarity calculations (`cosine_similarity`).
- **Uvicorn:** ASGI server for local development.

---

## 📁 Project Structure

```text
SmartFAQ/
├── api/
│   └── index.py        # FastAPI backend endpoint server
├── public/
│   └── index.html      # Responsive chatbot frontend UI
├── faq_data.json       # Structured local dataset containing sample FAQs
├── faq_engine.py       # Core matching engine (TF-IDF & Cosine Similarity)
├── nlp_utils.py        # Preprocessing & NLTK loader
├── requirements.txt    # Python backend dependencies
├── vercel.json         # Vercel deployment configuration
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

---

## 🚀 Local Development & Testing

### 1. Prerequisites
Ensure Python **3.8+** is installed on your system.

### 2. Clone / Navigate to Project Directory
```bash
cd SmartFAQ
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run FastAPI Backend Locally
```bash
uvicorn api.index:app --reload --port 8000
```

### 5. Access Frontend
Open `public/index.html` directly in your web browser, or serve it using any static file server.

---

## 🌐 Deploying to Vercel

1. Push all project files to your GitHub repository:
   ```bash
   git add .
   git commit -m "Convert SmartFAQ to Vercel compatible FastAPI fullstack app"
   git push origin main
   ```

2. Open [Vercel Dashboard](https://vercel.com/dashboard) and click **"Add New..." -> "Project"**.
3. Import your GitHub repository (`ramya792/-SmartFAQ`).
4. Select **Framework Preset**: `Other` (or leave default).
5. Click **Deploy**. Vercel will automatically detect `vercel.json` and deploy the Python API and static frontend.

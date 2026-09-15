# SmartFAQ – College FAQ Assistant

**CodeAlpha Internship – Task 2: Chatbot for FAQs**

SmartFAQ is a complete, beginner-friendly, professional, and offline **College FAQ Assistant** built with Python, Streamlit, NLTK, and Scikit-learn. It assists students, applicants, and parents by retrieving instant, accurate answers to common college queries regarding admissions, courses, fees, examinations, hostel facilities, placements, and campus services.

---

## 📌 Project Overview

Traditional college websites can be complex to navigate when seeking quick information. SmartFAQ simplifies this by allowing users to ask questions in plain English. The application processes the user query using Natural Language Processing (NLP), computes numerical text representations with **TF-IDF Vectorization**, and evaluates **Cosine Similarity** against a structured local dataset (`faq_data.json`) to return the most relevant answer without relying on any external AI API or paid internet service.

---

## 🎯 Key Features

- **100% Local & Free:** Runs completely offline without API keys, external LLM calls, or paid database dependencies.
- **Natural Language Preprocessing:** Uses NLTK for lowercasing, punctuation stripping, tokenization, stopword filtering, and WordNet lemmatization.
- **TF-IDF & Cosine Similarity Matching:** Computes vector similarity with a similarity threshold (`0.20`) to deliver accurate answers or polite fallback messages.
- **Interactive Streamlit Interface:** Features a modern chat UI with conversation history, suggested quick questions, clear chat controls, and responsive layout.
- **27 Sample FAQ Topics Covered:** Comprehensive default dataset covering admissions, courses, fees, exams, hostel, library, placements, certificates, and student services.
- **Safe & Modifiable Dataset:** Easily replace or extend `faq_data.json` with verified institution-specific FAQs.

---

## 🛠️ Technologies Used

- **Python:** Core programming language.
- **Streamlit:** Interactive web UI framework.
- **NLTK (Natural Language Toolkit):** Text preprocessing (tokenization, stopwords, lemmatization).
- **Scikit-learn:** TF-IDF vectorization (`TfidfVectorizer`) and cosine similarity calculations (`cosine_similarity`).
- **JSON:** Lightweight local storage for FAQ data.

---

## ⚙️ How the Chatbot Works

```text
User Question
      ↓
Text Preprocessing (Lowercasing, Punctuation Removal, Tokenization, Stopwords Removal, Lemmatization)
      ↓
TF-IDF Vectorization (Numerical vector representation)
      ↓
Cosine Similarity Calculation (Compare user vector against FAQ vectors)
      ↓
Best FAQ Match Selection (Evaluate against similarity threshold = 0.20)
      ↓
Display Answer (Return matched answer or polite fallback message)
```

---

## 📁 Project Structure

```text
SmartFAQ/
│
├── app.py              # Main Streamlit web application & user interface
├── faq_data.json       # Structured local dataset containing 27 sample FAQs
├── nlp_utils.py        # Text preprocessing functions & automatic NLTK resource downloader
├── faq_engine.py       # Core matching engine (TF-IDF, Cosine Similarity, threshold check)
├── requirements.txt   # Python dependency list
├── README.md           # Comprehensive project documentation
└── .gitignore          # Git ignore rules for virtual environments and cache files
```

### Purpose of Each File

- **`app.py`**: Manages the user interface, session state for chat history, click handlers for suggested questions, sidebar information, and layout formatting.
- **`faq_data.json`**: Stores pairs of `question` and `answer` items in clean JSON format.
- **`nlp_utils.py`**: Ensures NLTK resources (`stopwords`, `wordnet`, `omw-1.4`, `punkt`, `punkt_tab`) are downloaded automatically and converts raw text into clean, lemmatized tokens.
- **`faq_engine.py`**: Reads `faq_data.json`, vectorizes preprocessed text using Scikit-learn's `TfidfVectorizer`, calculates `cosine_similarity`, and selects the top answer above the similarity threshold (`0.20`).
- **`requirements.txt`**: Declares minimal dependencies (`streamlit`, `nltk`, `scikit-learn`).
- **`.gitignore`**: Excludes `venv/`, `__pycache__`, `.env`, and Streamlit temporary cache files from Git source control.

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have Python **3.8+** installed on your system.

### 2. Clone / Navigate to Project Directory
```bash
cd SmartFAQ
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**On Windows (PowerShell / Command Prompt):**
```bash
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
source venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Launch the Streamlit web server:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 💬 Example Questions to Try

1. **Admissions:** `How can I apply for admission?`
2. **Courses:** `What courses are offered?`
3. **Documents:** `What documents are required for admission?`
4. **Hostel:** `Does the college provide hostel facilities?`
5. **Library:** `What are the library timings?`
6. **Attendance:** `What is the minimum attendance requirement?`
7. **Exams:** `Where can I find the examination timetable?`
8. **Placements:** `Does the college provide placement assistance?`
9. **Internships:** `Are internship opportunities available for students?`
10. **Certificates:** `How can I get a bonafide certificate?`
11. **Password Reset:** `How do I reset my student portal password?`
12. **Out of Scope (Fallback Test):** `What is the weather today?` *(Returns friendly fallback message)*

---

## 📊 Sample Output Explanation

- **Exact / Synonymous Match:** When a user asks *"Can I get hostel accommodation?"*, the system matches keywords like `hostel` and returns the relevant FAQ answer regarding residential facilities.
- **Below Threshold Query:** When a user asks *"What is the weather today?"*, the cosine similarity score is `0.00` (below the `0.20` threshold). The chatbot politely responds:
  > *"Sorry, I could not find a suitable answer to your question. Please try asking in a different way or contact the college office for more information."*

---

## ⚠️ Limitations

- **Fixed Knowledge Base:** The chatbot can only answer questions present in or closely related to `faq_data.json`.
- **Exact Keyword Reliance:** As a statistical model (TF-IDF), it relies on overlapping vocabulary and root words (lemmas) rather than deep generative reasoning.
- **Sample Data Notice:** Information contained in `faq_data.json` is sample data and should be customized with verified institution data prior to official production deployment.

---

## 🔮 Future Improvements

- Add support for voice input and multi-language translation.
- Integrate fuzzy string matching for handling typos and spelling errors.
- Include administrative analytics dashboard to track common unanswered user queries.
- Expand dataset with department-specific FAQs.

---

## 📝 Disclaimer

*This project currently uses sample FAQ data. Please verify official college information with the college administration before taking action.*

---

**Developed for CodeAlpha Internship – Task 2**

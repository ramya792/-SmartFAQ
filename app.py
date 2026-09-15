# -*- coding: utf-8 -*-
"""
app.py
Streamlit Web Application for SmartFAQ \u2013 College FAQ Assistant.
Premium AI knowledge assistant interface.
"""

import streamlit as st
from faq_engine import load_faqs, get_best_answer
import base64
import io
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SmartFAQ Assistant",
    page_icon="\u2728",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global & Background */
.stApp {
    background-color: #fafafa;
    color: #1e293b;
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit UI */
header {visibility: hidden !important;}
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
[data-testid="stHeader"] {display: none !important;}

/* Adjust the main block container to act as the primary white panel */
[data-testid="stAppViewBlockContainer"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 900px;
    margin: 1.5rem auto;
}

/* 1. PREMIUM HEADER */
.premium-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.logo-box {
    background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);
}
.header-title-wrapper {
    display: flex;
    flex-direction: column;
}
.header-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
}
.header-subtitle {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 500;
}
.header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.status-indicator {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.85rem;
    color: #10b981;
    font-weight: 600;
    background: #ecfdf5;
    padding: 0.25rem 0.6rem;
    border-radius: 100px;
}
.status-dot {
    width: 8px;
    height: 8px;
    background-color: #10b981;
    border-radius: 50%;
}

/* 2. SPECIAL HERO SECTION */
.hero-wrapper {
    position: relative;
    text-align: center;
    padding: 1.5rem 0;
    margin-bottom: 1rem;
    overflow: hidden;
}
.hero-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(139,92,246,0.1) 0%, rgba(255,255,255,0) 70%);
    z-index: 0;
    pointer-events: none;
}
.hero-content {
    position: relative;
    z-index: 1;
}
.hero-heading {
    font-size: 2.75rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}
.hero-subheading {
    font-size: 1.05rem;
    color: #64748b;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* 3. CATEGORY NAVIGATION */
.category-section {
    margin-bottom: 1rem;
    text-align: center;
}
.category-title {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
/* Remove category-chip specific wrapping as it's no longer used */
.stButton > button {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 100px !important;
    color: #334155 !important;
    padding: 0.4rem 0.75rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.2rem !important; /* Smaller margin for buttons */
}
.stButton > button:hover {
    border-color: #8b5cf6 !important;
    color: #4f46e5 !important;
    box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.1) !important;
    transform: translateY(-1px);
}
/* Reduce Streamlit's default container gap on mobile */
[data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}

/* We removed the broken unclosed chat-panel-container div, and instead style the main container */
.chat-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 0.75rem;
    margin-bottom: 1rem;
}
.cph-left {
    display: flex;
    flex-direction: column;
}
.cph-title {
    font-weight: 700;
    color: #1e293b;
    font-size: 1.1rem;
}
.cph-subtitle {
    font-size: 0.8rem;
    color: #64748b;
}
.cph-badge {
    background: #f1f5f9;
    color: #64748b;
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-weight: 500;
    border: 1px solid #e2e8f0;
}

/* 5. CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 0 !important;
    gap: 0 !important;
}
[data-testid="chatAvatarIcon-user"], [data-testid="chatAvatarIcon-assistant"], .stChatMessageAvatar {
    display: none !important;
}

.chat-bubble-assistant-container {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 1rem;
    max-width: 90%;
}
.assistant-avatar {
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #4f46e5 0%, #8b5cf6 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.8rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
}
.chat-bubble-assistant {
    background-color: #f8fafc;
    color: #1e293b;
    padding: 0.75rem 1rem;
    border-radius: 4px 16px 16px 16px;
    font-size: 0.9rem;
    line-height: 1.4;
    border: 1px solid #e2e8f0;
}
.chat-bubble-user-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}
.chat-bubble-user {
    background-color: #4f46e5;
    background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 16px 4px 16px 16px;
    max-width: 85%;
    font-size: 0.9rem;
    line-height: 1.4;
    box-shadow: 0 2px 4px -1px rgba(0,0,0,0.1);
}

/* 7. SUGGESTED QUESTIONS inside chat panel */
.suggested-section-title {
    font-size: 0.85rem;
    color: #64748b;
    margin-bottom: 0.75rem;
    font-weight: 600;
}
.suggestion-btn .stButton > button {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    color: #475569 !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s !important;
}
.suggestion-btn .stButton > button:hover {
    border-color: #8b5cf6 !important;
    background-color: #faf5ff !important;
    color: #4f46e5 !important;
}

/* 6. QUESTION INPUT & BOTTOM CONTAINER */
[data-testid="stBottomBlockContainer"] {
    position: relative !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}
[data-testid="stChatInput"] {
    background-color: #ffffff !important;
    border-radius: 24px !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
    padding: 0.25rem !important;
    padding-right: 5rem !important; /* Room for mic and send buttons */
    margin-top: 0.5rem;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
}
[data-testid="stChatInput"] textarea {
    font-size: 1rem !important;
    color: #1e293b !important;
}

/* SLEEK MIC BUTTON OVERLAY */
.st-key-STT_icon {
    position: absolute !important;
    right: 3.8rem !important;
    bottom: 0.85rem !important;
    z-index: 99999 !important;
    width: 36px !important;
    height: 36px !important;
}
.st-key-STT_icon iframe {
    border: none !important;
    background: transparent !important;
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
}
.st-key-STT_icon button {
    background: #f1f5f9 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
    transition: all 0.2s ease-in-out !important;
}
.st-key-STT_icon button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    border-color: #4f46e5 !important;
    color: white !important;
    transform: scale(1.08) !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}
@media (max-width: 600px) {
    .st-key-STT_icon {
        right: 3.5rem !important;
        bottom: 0.75rem !important;
    }
}

/* 9. VOICE MODE STYLING */
.voice-mode-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 45vh;
    text-align: center;
    padding: 1.5rem 1rem 0.5rem 1rem;
    position: relative;
}
.voice-orb-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 1.5rem 0;
}
.voice-orb-glow {
    position: absolute;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.1) 60%, rgba(255,255,255,0) 80%);
    border-radius: 50%;
    animation: pulse-glow 2.5s infinite ease-in-out;
    pointer-events: none;
    z-index: 0;
}
@keyframes pulse-glow {
    0% { transform: scale(0.9); opacity: 0.5; }
    50% { transform: scale(1.25); opacity: 0.95; }
    100% { transform: scale(0.9); opacity: 0.5; }
}
.voice-title {
    font-size: 1.75rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}
.voice-subtitle {
    font-size: 0.95rem;
    color: #64748b;
    margin-bottom: 1rem;
    max-width: 420px;
    line-height: 1.4;
}
.voice-transcript-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    max-width: 600px;
    width: 100%;
    margin-top: 1.5rem;
    text-align: left;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}
.voice-transcript-user {
    font-size: 0.85rem;
    color: #4f46e5;
    font-weight: 700;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.voice-transcript-user-text {
    font-size: 1rem;
    color: #1e293b;
    font-weight: 600;
    margin-bottom: 0.75rem;
}
.voice-transcript-bot {
    font-size: 0.85rem;
    color: #8b5cf6;
    font-weight: 700;
    margin-bottom: 0.2rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.voice-transcript-bot-text {
    font-size: 0.95rem;
    color: #334155;
    line-height: 1.5;
}

/* Custom styling for STT inside Voice Mode */
.st-key-STT_voice_mode {
    position: relative !important;
    z-index: 2 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin: 0 auto !important;
}
.st-key-STT_voice_mode button {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    box-shadow: 0 10px 25px rgba(79, 70, 229, 0.4) !important;
    transition: all 0.3s ease !important;
}
.st-key-STT_voice_mode button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 14px 30px rgba(79, 70, 229, 0.5) !important;
}

/* Mobile Adjustments */
@media (max-width: 600px) {
    [data-testid="stAppViewBlockContainer"] {
        padding: 1rem 0.75rem 2rem 0.75rem !important;
    }
    .header-title {
        font-size: 1rem;
    }
    .hero-heading {
        font-size: 2rem;
    }
    .hero-subheading {
        font-size: 0.95rem;
        padding: 0 0.5rem;
    }
    .chat-panel-container {
        padding: 1.25rem;
        border-radius: 16px;
    }
    .cph-title {
        font-size: 0.95rem;
    }
    .cph-subtitle {
        display: none;
    }
    .feature-glance {
        flex-direction: column;
        gap: 1.5rem;
    }
    .voice-title {
        font-size: 1.4rem;
    }
}
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
FAQS = load_faqs("faq_data.json")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! \U0001f44b\n\nI\u2019m your SmartFAQ College Assistant. I can help you find information about admissions, courses, fees, examinations, hostel, library, internships, and placements.\n\nWhat would you like to know?"
        }
    ]
if "voice_mode_active" not in st.session_state:
    st.session_state.voice_mode_active = False
if "last_audio_b64" not in st.session_state:
    st.session_state.last_audio_b64 = None

# --- 9. SIDEBAR ---
with st.sidebar:
    st.markdown("### \u2728 SmartFAQ")
    st.caption("College Knowledge Assistant")
    st.markdown("---")
    
    st.markdown("#### Interface Mode")
    if st.session_state.voice_mode_active:
        if st.button("\U0001f4ac Switch to Text Chat", use_container_width=True, key="sb_btn_text"):
            st.session_state.voice_mode_active = False
            st.rerun()
    else:
        if st.button("\U0001f399\ufe0f Switch to Voice Mode", use_container_width=True, key="sb_btn_voice"):
            st.session_state.voice_mode_active = True
            st.rerun()

    st.markdown("---")
    st.markdown("#### About the project")
    st.write("SmartFAQ is an intelligent college companion that uses local NLP (NLTK, TF-IDF, Cosine Similarity) to instantly find answers to common questions.")
    
    st.markdown("#### Topics covered")
    st.write("Admissions, Courses, Fees, Scholarships, Attendance, Examinations, Hostel, Library, Internships, Placements, Certificates, Student services.")
    
    st.markdown("#### How it works")
    st.markdown("1. User asks a question\n2. Text is preprocessed\n3. FAQ similarity is calculated\n4. Best answer is displayed")
    
    st.markdown("---")
    if st.button("\U0001f5d1\ufe0f Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! \U0001f44b\n\nI\u2019m your SmartFAQ College Assistant. I can help you find information about admissions, courses, fees, examinations, hostel, library, internships, and placements.\n\nWhat would you like to know?"
            }
        ]
        st.rerun()
        
    st.markdown("#### Settings")
    if 'enable_voice' not in st.session_state:
        st.session_state.enable_voice = True
    st.session_state.enable_voice = st.toggle("Enable Voice Responses", value=st.session_state.enable_voice)
    
    st.markdown("---")
    
    chat_text = "SmartFAQ Chat History\n" + "="*20 + "\n\n"
    for m in st.session_state.messages:
        role = "You" if m["role"] == "user" else "Assistant"
        chat_text += f"{role}: {m['content']}\n\n"
    
    b64 = base64.b64encode(chat_text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="chat_history.txt" style="display: block; text-align: center; text-decoration: none; padding: 0.5rem; background: #ffffff; color: #4f46e5; border: 1px solid #e2e8f0; border-radius: 100px; font-size: 0.85rem; font-weight: 500;">\U0001f4e5 Download Chat History</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Demo version using sample FAQ data. Verify official information with the college administration.")

# Selected question tracker
selected_suggested_q = None

# --- 1. PREMIUM HEADER ---
hdr_col1, hdr_col2 = st.columns([3, 1])
with hdr_col1:
    st.markdown("""
    <div class="premium-header" style="border-bottom: none; margin-bottom: 0; padding-bottom: 0;">
        <div class="header-left">
            <div class="logo-box">&#10022;</div>
            <div class="header-title-wrapper">
                <div class="header-title">SmartFAQ</div>
                <div class="header-subtitle">College Knowledge Assistant</div>
            </div>
            <div class="status-indicator" style="margin-left: 0.5rem;">
                <div class="status-dot"></div>
                Online
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with hdr_col2:
    if st.session_state.voice_mode_active:
        if st.button("\U0001f4ac Text Mode", key="hdr_mode_btn", use_container_width=True):
            st.session_state.voice_mode_active = False
            st.rerun()
    else:
        if st.button("\U0001f399\ufe0f Voice Mode", key="hdr_mode_btn", use_container_width=True):
            st.session_state.voice_mode_active = True
            st.rerun()

st.markdown('<div style="border-bottom: 1px solid #e5e7eb; margin-bottom: 1rem; margin-top: 0.5rem;"></div>', unsafe_allow_html=True)

# --- MESSAGES & TTS HELPER FUNCTIONS ---
def render_message(role, content):
    content = content.replace('\n', '<br>')
    if role == "user":
        st.markdown(f"""
        <div class="chat-bubble-user-container">
            <div class="chat-bubble-user">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-bubble-assistant-container">
            <div class="assistant-avatar">&#10022;</div>
            <div class="chat-bubble-assistant">{content}</div>
        </div>
        """, unsafe_allow_html=True)

def process_user_query(query_text: str):
    if not query_text or not query_text.strip():
        return
    st.session_state.messages.append({"role": "user", "content": query_text})

    result = get_best_answer(query_text, FAQS, threshold=0.20)
    bot_reply = result["answer"]

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
    if st.session_state.get('enable_voice', True):
        try:
            tts = gTTS(bot_reply, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            b64 = base64.b64encode(fp.read()).decode()
            st.session_state.last_audio_b64 = b64
        except Exception as e:
            print(f"TTS Error: {e}")

# Play audio autoplay tag if set
if st.session_state.get("last_audio_b64"):
    st.markdown(f"""
        <audio autoplay="true" style="display:none;">
        <source src="data:audio/mp3;base64,{st.session_state.last_audio_b64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)
    st.session_state.last_audio_b64 = None

# --- CONDITIONAL INTERFACE RENDER ---
if st.session_state.voice_mode_active:
    # --- DEDICATED FULL-SCREEN VOICE MODE VIEW ---
    st.markdown("""
    <div class="voice-mode-wrapper">
        <div class="voice-title">Realtime Voice Mode</div>
        <div class="voice-subtitle">Tap the microphone below and speak your college question out loud.</div>
        <div class="voice-orb-container">
            <div class="voice-orb-glow"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    voice_input = speech_to_text(
        language='en',
        start_prompt="\U0001f399\ufe0f Tap to Speak",
        stop_prompt="\u23f9\ufe0f Listening...",
        just_once=True,
        key='STT_voice_mode'
    )

    # Check for voice input either returned directly or via session_state key
    raw_voice = voice_input or st.session_state.get('STT_voice_mode_output')
    if raw_voice:
        if isinstance(raw_voice, dict):
            raw_voice = raw_voice.get('text') or raw_voice.get('transcript') or ''
        if isinstance(raw_voice, str) and raw_voice.strip():
            st.session_state['STT_voice_mode_output'] = None
            process_user_query(raw_voice.strip())
            st.rerun()

    # Show transcript of recent interaction
    if len(st.session_state.messages) > 1:
        last_user_msg = None
        last_bot_msg = None
        for m in reversed(st.session_state.messages):
            if m["role"] == "assistant" and not last_bot_msg:
                last_bot_msg = m["content"]
            elif m["role"] == "user" and not last_user_msg:
                last_user_msg = m["content"]
            if last_user_msg and last_bot_msg:
                break
        
        if last_user_msg and last_bot_msg:
            st.markdown(f"""
            <div style="display: flex; justify-content: center;">
                <div class="voice-transcript-card">
                    <div class="voice-transcript-user">\U0001f5e3\ufe0f You Asked</div>
                    <div class="voice-transcript-user-text">{last_user_msg}</div>
                    <div class="voice-transcript-bot">\U0001f916 Assistant Reply</div>
                    <div class="voice-transcript-bot-text">{last_bot_msg}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 1rem;">\U0001f4a1 Tip: Click <b>Tap to Speak</b>, grant microphone permissions if prompted by your browser, and speak your question clearly.</div>', unsafe_allow_html=True)

else:
    # --- STANDARD TEXT CHAT VIEW ---
    if len(st.session_state.messages) <= 1:
        st.markdown("""
        <div class="hero-wrapper">
            <div class="hero-glow"></div>
            <div class="hero-content">
                <div class="hero-heading">Your college questions,<br>answered simply.</div>
                <div class="hero-subheading">Get quick answers about admissions, academics, campus life, and career opportunities.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- CATEGORY NAVIGATION ---
        st.markdown('<div class="category-section"><div class="category-title">Explore topics</div></div>', unsafe_allow_html=True)
        
        cat1, cat2, cat3 = st.columns(3)
        with cat1:
            if st.button("\U0001f4dd Admissions", use_container_width=True): selected_suggested_q = "How can I apply for admission?"
        with cat2:
            if st.button("\U0001f4da Academics", use_container_width=True): selected_suggested_q = "What courses are offered?"
        with cat3:
            if st.button("\U0001f4dd Exams", use_container_width=True): selected_suggested_q = "Where can I find the examination timetable?"
            
        cat4, cat5, cat6 = st.columns(3)
        with cat4:
            if st.button("\U0001f3eb Campus Life", use_container_width=True): selected_suggested_q = "Does the college provide hostel facilities?"
        with cat5:
            if st.button("\U0001f6e0\ufe0f Services", use_container_width=True): selected_suggested_q = "How can I get a bonafide certificate?"
        with cat6:
            if st.button("\U0001f4bc Placements", use_container_width=True): selected_suggested_q = "Does the college provide placement assistance?"

    # --- MAIN CHAT CONTAINER ---
    st.markdown("""
    <div class="chat-panel-header">
        <div class="cph-left">
            <div class="cph-title">\U0001f916 SmartFAQ Assistant</div>
            <div class="cph-subtitle">Ask questions from our college FAQ knowledge base</div>
        </div>
        <div class="cph-right">
            <span class="cph-badge">Local knowledge base</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            render_message(message["role"], message["content"])

    # Suggested Questions inside Chat Panel
    if len(st.session_state.messages) <= 1:
        st.markdown('<div class="suggested-section-title">Try asking</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("How can I apply for admission?", use_container_width=True): selected_suggested_q = "How can I apply for admission?"
            if st.button("Does the college provide hostel facilities?", use_container_width=True): selected_suggested_q = "Does the college provide hostel facilities?"
            if st.button("Does the college provide placement assistance?", use_container_width=True): selected_suggested_q = "Does the college provide placement assistance?"
        with col2:
            if st.button("What courses are offered?", use_container_width=True): selected_suggested_q = "What courses are offered?"
            if st.button("What is the attendance requirement?", use_container_width=True): selected_suggested_q = "What is the minimum attendance requirement?"

    # Question Input
    user_input = st.chat_input("Ask anything about your college...")

    spoken_text = speech_to_text(
        language='en',
        start_prompt="\U0001f3a4",
        stop_prompt="\u23f9\ufe0f",
        just_once=True,
        key='STT_icon'
    )

    raw_spoken = spoken_text or st.session_state.get('STT_icon_output')
    if raw_spoken and isinstance(raw_spoken, dict):
        raw_spoken = raw_spoken.get('text') or raw_spoken.get('transcript') or ''

    if selected_suggested_q:
        process_user_query(selected_suggested_q)
        st.rerun()
    elif user_input:
        process_user_query(user_input)
        st.rerun()
    elif raw_spoken and isinstance(raw_spoken, str) and raw_spoken.strip():
        st.session_state['STT_icon_output'] = None
        process_user_query(raw_spoken.strip())
        st.rerun()

    # Feature Glance
    if len(st.session_state.messages) <= 1:
        st.markdown("""
        <div class="feature-glance">
            <div class="feature-item">
                <div class="feature-value">25+</div>
                <div class="feature-label">Sample FAQs</div>
            </div>
            <div class="feature-item">
                <div class="feature-value">6+</div>
                <div class="feature-label">Topic Areas</div>
            </div>
            <div class="feature-item">
                <div class="feature-value">24/7</div>
                <div class="feature-label">Instant Access</div>
            </div>
        </div>
        <div class="glance-disclaimer">
            Demo version using sample FAQ data. Verify official information with the college administration.
        </div>
        """, unsafe_allow_html=True)


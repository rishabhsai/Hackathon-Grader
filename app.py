import streamlit as st
from judge import run_evaluation, run_evaluation_text
import tempfile
import PyPDF2
import openai
import requests
import streamlit.components.v1 as components

SAPLING_API_KEY = "AOM37012AEROXNPALYM7E6ZEX2CPZVEC"

# --- Session State Initialization ---
if "ai_analysis" not in st.session_state:
    st.session_state["ai_analysis"] = None
if "submission_text" not in st.session_state:
    st.session_state["submission_text"] = None

def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def detect_ai_generated(text):
    url = "https://api.sapling.ai/api/v1/aidetect"
    headers = {"Content-Type": "application/json"}
    data = {
        "key": SAPLING_API_KEY,
        "text": text,
        "sent_scores": True,
        "score_string": True
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return None

st.set_page_config(
    page_title="AI Hackathon Grading Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/',
        'Report a bug': 'https://github.com/'
    }
)

# Custom CSS for dark theme, shadcn-inspired look, and subtle animations
st.markdown('''
    <style>
    body, .stApp {
        background: #18181b !important;
        color: #f4f4f5 !important;
        font-family: 'Inter', 'Segoe UI', 'sans-serif';
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a21caf 100%);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0.75em 2em;
        font-size: 1.1em;
        font-weight: 600;
        box-shadow: 0 2px 16px #a21caf22;
        transition: transform 0.15s, box-shadow 0.15s;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 4px 24px #a21caf44;
    }
    .stFileUploader>div>div {
        background: #27272a !important;
        border-radius: 8px !important;
        border: 1.5px solid #6366f1 !important;
        color: #f4f4f5 !important;
        font-size: 1.05em;
    }
    .stMarkdown, .stSpinner {
        animation: fadeIn 0.7s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: none; }
    }
    </style>
''', unsafe_allow_html=True)

# --- Routing ---
def main_page():
    st.markdown("""
    # 🤖 AI Hackathon Grading Assistant
    Welcome to the AI-powered Hackathon Grading Assistant! 🚀
    **How it works:**
    - Upload your project submission as a Markdown (`.md`), text (`.txt`), or PDF (`.pdf`) file.
    - The AI will evaluate your submission against the official rubric.
    - You'll receive detailed, category-wise feedback and a final score.
    *Powered by GPT-4o. Your data is processed securely and not stored.*
    """)
    uploaded_file = st.file_uploader(
        "Upload your hackathon submission (.md, .txt, or .pdf)",
        type=["md", "txt", "pdf"],
        help="Markdown, plain text, or PDF files are supported.",
        key="file_uploader"
    )
    if uploaded_file:
        if st.button("✨ Evaluate Submission"):
            with st.spinner('Checking for AI-generated content...'):
                try:
                    if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                        submission_text = extract_pdf_text(uploaded_file)
                    else:
                        submission_text = uploaded_file.read().decode("utf-8")
                    ai_result = detect_ai_generated(submission_text)
                    if ai_result:
                        score = ai_result.get("score", 0)
                        st.info(f"AI Probability: {score*100:.1f}% (0 = human, 100 = AI)")
                        # Store details in session state for navigation
                        st.session_state["ai_analysis"] = ai_result
                        st.session_state["submission_text"] = submission_text
                    with st.spinner('The AI grader is deliberating...'):
                        if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                            result = run_evaluation_text(submission_text)
                        else:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp:
                                tmp.write(submission_text.encode("utf-8"))
                                tmp_path = tmp.name
                            result = run_evaluation(tmp_path)
                        try:
                            st.markdown(result, unsafe_allow_html=True)
                            # Fallback: if the result is not None and looks like markdown but doesn't render, also show with st.write
                            if result and (result.strip().startswith("#") or result.strip().startswith("|")):
                                st.write(result)
                        except Exception:
                            st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        # Clear session state if a new file is uploaded
        if st.session_state.get("last_uploaded_filename") != uploaded_file.name:
            st.session_state["ai_analysis"] = None
            st.session_state["submission_text"] = None
            st.session_state["last_uploaded_filename"] = uploaded_file.name

    # --- AI Sentence Analysis & Highlighting (Collapsible) ---
    ai_result = st.session_state.get("ai_analysis")
    if ai_result:
        with st.expander("🔍 AI Sentence Analysis & Highlighting", expanded=False):
            score = ai_result.get("score", 0)
            st.info(f"Overall AI Probability: {score*100:.1f}% (0 = human, 100 = AI)")
            # Sentence-level table
            st.markdown("## Sentence-level AI Probability")
            sentence_scores = ai_result.get("sentence_scores", [])
            if sentence_scores:
                import pandas as pd
                df = pd.DataFrame(sentence_scores)
                df["AI Probability %"] = df["score"].apply(lambda x: f"{x*100:.1f}%")
                st.dataframe(df[["sentence", "AI Probability %"]], use_container_width=True)
            else:
                st.write("No sentence-level scores available.")
            # Highlighted HTML
            st.markdown("## Highlighted AI-generated Text")
            score_string = ai_result.get("score_string")
            if score_string:
                st.markdown("""
                <style>
                .sapling-highlighted-html, .sapling-highlighted-html * {
                    color: #fff !important;
                }
                </style>
                """, unsafe_allow_html=True)
                components.html(score_string, height=300, scrolling=True)
            else:
                st.write("No highlight available.")

# --- Page Routing ---
if "page" not in st.session_state:
    st.session_state["page"] = "main"

main_page() 
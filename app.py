import streamlit as st
from judge import run_evaluation, run_evaluation_text
import tempfile
import PyPDF2

def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

st.set_page_config(
    page_title="AI Hackathon Judge",
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

st.markdown("""
# 🤖 AI Hackathon Judge

Welcome to the AI-powered Hackathon Judge! 🚀

**How it works:**
- Upload your project submission as a Markdown (`.md`), text (`.txt`), or PDF (`.pdf`) file.
- The AI will evaluate your submission against the official rubric.
- You'll receive detailed, category-wise feedback and a final score.

*Powered by GPT-4o. Your data is processed securely and not stored.*
""")

uploaded_file = st.file_uploader(
    "Upload your hackathon submission (.md, .txt, or .pdf)",
    type=["md", "txt", "pdf"],
    help="Markdown, plain text, or PDF files are supported."
)

if uploaded_file:
    if st.button("✨ Evaluate Submission"):
        with st.spinner('The AI judge is deliberating...'):
            try:
                if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                    submission_text = extract_pdf_text(uploaded_file)
                    result = run_evaluation_text(submission_text)
                else:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name
                    result = run_evaluation(tmp_path)
                st.markdown(result, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}") 
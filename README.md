# AI Hackathon Judge

A modern, AI-powered tool to automatically grade hackathon submissions (Markdown, text, or PDF) against a rubric using OpenAI's GPT-4o. Features a beautiful, dark-themed Streamlit web interface inspired by shadcn UI.

---

## 🚀 Features
- **Automatic Grading:** Uses GPT-4o to evaluate submissions based on your rubric.
- **PDF, Markdown, and Text Support:** Upload `.pdf`, `.md`, or `.txt` files.
- **Modern Web UI:** Elegant, animated, dark-themed interface.
- **Command-Line Tool:** Grade submissions from your terminal.
- **Granular Git History:** Each file is committed separately for easy tracking.

---

## 🛠️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rishabhsai/Hackathon-Grader.git
   cd hackathon_grader
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add your OpenAI API key:**
   - Create a `.env` file in the project root (if not present).
   - Add this line (replace with your key):
     ```
     OPENAI_API_KEY="sk-..."
     ```

---

## 💻 Usage

### 1. **Web App**
Run the Streamlit app:
```bash
.venv/bin/streamlit run app.py
```
- Open the local URL (e.g., http://localhost:8501) in your browser.
- Upload a `.pdf`, `.md`, or `.txt` file and click "✨ Evaluate Submission".
- The AI will grade your submission and display detailed feedback.

### 2. **Command-Line Tool**
Grade a submission from the terminal:
```bash
.venv/bin/python judge.py path/to/your_submission.md
```
- Replace with your file path. Output will be printed to the console.

---

## 📄 Rubric & Prompt
- **rubric.md:** Edit this file to define your judging criteria.
- **prompt_template.txt:** Edit this to change the AI's instructions.

---

## 📝 Sample PDFs
- See the `sample pdfs/` folder for example submissions you can test.


---

## 📢 Credits
- Built with [Streamlit](https://streamlit.io/), [OpenAI](https://platform.openai.com/), and [PyPDF2](https://pypdf2.readthedocs.io/).
- UI inspired by [shadcn/ui](https://ui.shadcn.com/).

---

## 🛡️ License
MIT License. See `LICENSE` file for details. 

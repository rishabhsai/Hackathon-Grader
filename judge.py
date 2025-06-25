import os
import argparse
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def run_evaluation(submission_path):
    with open("rubric.md", "r") as f:
        rubric = f.read()
    with open(submission_path, "r") as f:
        submission = f.read()
    with open("prompt_template.txt", "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.replace("{rubric}", rubric).replace("{submission}", submission)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.2,
    )
    return response.choices[0].message.content


def run_evaluation_text(submission_text):
    with open("rubric.md", "r") as f:
        rubric = f.read()
    with open("prompt_template.txt", "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.replace("{rubric}", rubric).replace("{submission}", submission_text)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.2,
    )
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="AI Hackathon Judge")
    parser.add_argument("submission_path", type=str, help="Path to the submission file (.md or .txt)")
    args = parser.parse_args()
    result = run_evaluation(args.submission_path)
    print(result)

if __name__ == "__main__":
    main() 
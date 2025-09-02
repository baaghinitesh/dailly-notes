import os
import random
import sys
import json
import git
import google.generativeai as genai
import datetime

# ------------------ Get config from environment variables ------------------
API_KEY = os.environ.get("API_KEY")
AUTHOR_NAME = os.environ.get("AUTHOR_NAME")
AUTHOR_EMAIL = os.environ.get("AUTHOR_EMAIL")

if not API_KEY or not AUTHOR_NAME or not AUTHOR_EMAIL:
    print("Error: Make sure to set API_KEY, AUTHOR_NAME, and AUTHOR_EMAIL environment variables.")
    sys.exit(1)

# ------------------ Gemini setup ------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Load topics ------------------
def load_topics():
    with open("topics.json", "r", encoding="utf-8") as f:
        return json.load(f)

topics = load_topics()

# ------------------ AI Content Generator ------------------
def generate_content(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No response generated."
    except Exception as e:
        return f"Error generating content: {e}"

# ------------------ Pickers with Duplicate Check ------------------
def pick_dsa_question():
    attempts = 0
    max_attempts = 20  # Prevent infinite loops if all topics are covered
    while attempts < max_attempts:
        difficulty = random.choice(["easy", "medium", "hard"])
        question = random.choice(topics[difficulty])
        file_name = f"dsa/{difficulty}/{question.replace(' ', '')}.java"
        if not os.path.exists(file_name):
            return difficulty, question
        attempts += 1
    print("Could not find a new DSA question after several attempts. Skipping.")
    return None, None

def pick_note_topic():
    attempts = 0
    max_attempts = 20
    while attempts < max_attempts:
        section = random.choice(list(topics["notes"].keys()))
        note = random.choice(topics["notes"][section])
        file_name = f"notes/{section}/{note.replace(' ', '_')}.md"
        if not os.path.exists(file_name):
            return section, note
        attempts += 1
    print("Could not find a new note topic after several attempts. Skipping.")
    return None, None

# ------------------ File + Git ------------------
def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def commit_and_push(file_paths: list, message: str):
    repo = git.Repo(".")
    for file_path in file_paths:
        repo.git.add(file_path)
    repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
    origin = repo.remote(name="origin")
    origin.push()

# ------------------ Task ------------------
def daily_task():
    if random.choice([True, False]):
        difficulty, question = pick_dsa_question()
        if not question: # If no new question was found, exit gracefully
            print("Skipping DSA task as no new question was found.")
            sys.exit(0)

        java_prompt = (
            f"Provide a well-formatted Java solution for the problem: '{question}'.\n"
            f"The class name must be the problem name in CamelCase (e.g., TwoSum).\n"
            f"Include the question and difficulty as a comment at the top.\n"
            f"IMPORTANT: Respond with ONLY the raw Java code. Do not include any extra text or markdown formatting."
        )
        java_solution = generate_content(java_prompt)
        java_solution = java_solution.replace("```java", "").replace("```", "").strip()

        summary_prompt = (
            f"Provide a brief summary and complexity analysis for the Java solution to the problem: {question}.\n"
            f"Format the answer as follows:\n\n"
            f"## Summary of Approach\n...\n\n"
            f"## Time and Space Complexity\n- Time Complexity: O(...)\n- Space Complexity: O(...)"
        )
        summary_content = generate_content(summary_prompt)

        file_name_base = question.replace(' ', '')
        java_file_name = f"dsa/{difficulty}/{file_name_base}.java"
        summary_file_name = f"dsa/{difficulty}/{file_name_base}.md"

        save_file(java_file_name, java_solution)
        save_file(summary_file_name, summary_content)

        commit_and_push([java_file_name, summary_file_name], f"Added DSA solution: {question}")
        print(f"✅ DSA solution added: {question}")

    else:
        section, note = pick_note_topic()
        if not note: # If no new note topic was found, exit gracefully
            print("Skipping notes task as no new topic was found.")
            sys.exit(0)

        prompt = (
            f"# In-Depth Study Notes: {note}\n\n"
            "Provide a comprehensive, premium-quality note on the topic. Include these sections:\n"
            "## 1. Introduction\n## 2. Core Concepts\n## 3. Practical Examples\n## 4. Conclusion"
        )
        content = generate_content(prompt)
        file_name = f"notes/{section}/{note.replace(' ', '_')}.md"
        save_file(file_name, content)
        commit_and_push([file_name], f"Added notes: {note}")
        print(f"✅ Notes added: {note}")

# ------------------ Run ------------------
if __name__ == "__main__":
    daily_task()

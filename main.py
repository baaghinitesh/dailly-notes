import os
import random
import sys
import json
import git
import google.generativeai as genai
import datetime
from config import API_KEY, GITHUB_REPO, AUTHOR_NAME, AUTHOR_EMAIL

# ------------------ Run Control ------------------
def should_run():
    today = datetime.date.today().isoformat()
    state_file = ".run_state"

    runs_today = 0
    last_date = None

    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            last_date, runs_today = f.read().split(",")
            runs_today = int(runs_today)

    if last_date != today:
        runs_today = 0

    if runs_today >= 2:
        return False, today, runs_today

    chance = random.random()
    if chance < 0.1:  # ~10% chance each hour
        runs_today += 1
        with open(state_file, "w") as f:
            f.write(f"{today},{runs_today}")
        return True, today, runs_today
    else:
        with open(state_file, "w") as f:
            f.write(f"{today},{runs_today}")
        return False, today, runs_today


if __name__ == "__main__":
    run, today, runs = should_run()
    if not run:
        print(f"⏭️ Skipping run. Date={today}, Runs so far={runs}")
        sys.exit(0)

# ------------------ Gemini setup ------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")  # free + fast

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

# ------------------ Pickers ------------------
def pick_dsa_question():
    difficulty = random.choice(["easy", "medium", "hard"])
    question = random.choice(topics[difficulty])
    return difficulty, question

def pick_note_topic():
    section = random.choice(list(topics["notes"].keys()))
    note = random.choice(topics["notes"][section])
    return section, note

# ------------------ File + Git ------------------
def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def commit_and_push(file_path: str, message: str):
    repo = git.Repo(".")
    repo.git.add(file_path)
    repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
    origin = repo.remote(name="origin")
    origin.push()

# ------------------ Task ------------------
def daily_task():
    if random.choice([True, False]):
        difficulty, question = pick_dsa_question()
        prompt = f"Solve this DSA problem in Python with explanation:\n\n{question}"
        content = generate_content(prompt)
        file_name = f"dsa/{difficulty}/{question.replace(' ', '_')}.txt"
        save_file(file_name, content)
        commit_and_push(file_name, f"Added DSA solution: {question}")
        print(f"✅ DSA solution added: {question}")
    else:
        section, note = pick_note_topic()
        prompt = f"Write detailed study notes on: {note}"
        content = generate_content(prompt)
        file_name = f"notes/{section}/{note.replace(' ', '_')}.txt"
        save_file(file_name, content)
        commit_and_push(file_name, f"Added notes: {note}")
        print(f"✅ Notes added: {note}")

# ------------------ Run ------------------
daily_task()

import os
import random
import sys
import json
import git
import google.generativeai as genai

# ------------------ Get config ------------------
API_KEY = os.environ.get("API_KEY")
AUTHOR_NAME = os.environ.get("AUTHOR_NAME")
AUTHOR_EMAIL = os.environ.get("AUTHOR_EMAIL")

if not API_KEY or not AUTHOR_NAME or not AUTHOR_EMAIL:
    print("❌ Missing required environment variables.")
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
        return response.text.strip() if response.text else "⚠️ No response generated."
    except Exception as e:
        return f"⚠️ Error generating content: {e}"

# ------------------ Pickers ------------------
def pick_new_file(path, candidates, format_name):
    """Ensure we always generate a new file that doesn’t exist yet"""
    random.shuffle(candidates)
    for candidate in candidates:
        fname = format_name(candidate)
        if not os.path.exists(fname):
            return candidate, fname
    return None, None

def pick_dsa_question():
    difficulty = random.choice(["easy", "medium", "hard"])
    candidates = topics[difficulty]
    return pick_new_file(
        f"docs/dsa/{difficulty}/",
        candidates,
        lambda q: f"docs/dsa/{difficulty}/{q.replace(' ', '')}"
    )

def pick_note_topic():
    section = random.choice(list(topics["notes"].keys()))
    candidates = topics["notes"][section]
    return pick_new_file(
        f"docs/notes/{section}/",
        candidates,
        lambda n: f"docs/notes/{section}/{n.replace(' ', '_')}.md"
    )

# ------------------ File + Git ------------------
def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def commit_and_push(file_paths: list, message: str):
    repo = git.Repo(".")
    for fp in file_paths:
        repo.git.add(fp)
    repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
    repo.remote(name="origin").push()

# ------------------ Tasks ------------------
def add_dsa():
    question, base_path = pick_dsa_question()
    if not question:
        print("⚠️ No new DSA question found.")
        return False

    java_prompt = (
        f"Provide a Java solution for: '{question}'.\n"
        f"Class name = problem name in CamelCase.\n"
        f"Include question + difficulty as comments.\n"
        f"Respond ONLY with raw Java code."
    )
    java_solution = generate_content(java_prompt).replace("```java", "").replace("```", "").strip()

    summary_prompt = (
        f"Write summary + complexity for: {question}.\n"
        "Format:\n## Summary of Approach\n...\n\n## Time and Space Complexity\n- Time: O(...)\n- Space: O(...)"
    )
    summary_content = generate_content(summary_prompt)

    java_file = f"{base_path}.java"
    md_file = f"{base_path}.md"

    save_file(java_file, java_solution)
    save_file(md_file, summary_content)
    commit_and_push([java_file, md_file], f"📘 Added DSA solution: {question}")
    print(f"✅ DSA solution added: {question}")
    return True

def add_note():
    note, file_path = pick_note_topic()
    if not note:
        print("⚠️ No new note topic found.")
        return False

    prompt = (
        f"# {note}\n\n"
        "Write premium-quality study notes:\n"
        "## 1. Introduction\n## 2. Core Concepts\n## 3. Practical Examples\n## 4. Conclusion"
    )
    content = generate_content(prompt)

    save_file(file_path, content)
    commit_and_push([file_path], f"📝 Added note: {note}")
    print(f"✅ Note added: {note}")
    return True

# ------------------ Run ------------------
if __name__ == "__main__":
    # Always generate both (guaranteed 2 pushes/day)
    added_dsa = add_dsa()
    added_note = add_note()

    if not added_dsa and not added_note:
        print("⚠️ Nothing new could be generated today.")

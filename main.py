#!/usr/bin/env python3
"""
Fixed main.py for Auto DSA + Notes + Deploy
- Ensures candidates are lists before random.shuffle
- Flattens nested 'notes' sections in topics.json
- Manual runs (workflow_dispatch): run immediately, allow RUN_COUNT
- Push runs: run immediately (no delay)
- Scheduled runs: random delay (up to 3 hours)
- Adds API timeout to prevent hangs
"""

import os
import random
import sys
import json
import time
import git
import signal
import google.generativeai as genai
from typing import Any, List, Iterable

# ------------------ Get config ------------------
API_KEY = os.environ.get("API_KEY")
AUTHOR_NAME = os.environ.get("AUTHOR_NAME")
AUTHOR_EMAIL = os.environ.get("AUTHOR_EMAIL")

if not API_KEY or not AUTHOR_NAME or not AUTHOR_EMAIL:
    print("❌ Missing required environment variables: API_KEY / AUTHOR_NAME / AUTHOR_EMAIL")
    sys.exit(1)

# ------------------ Gemini setup ------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Load topics ------------------
TOPICS_FILE = "topics.json"

def load_topics():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

topics = load_topics()

# ------------------ Helpers ------------------
def flatten_to_strings(value: Any) -> List[str]:
    """
    Recursively flatten nested structures in topics.json to a list of strings.
    Handles lists, dicts (keys or values), and nested dict/list combos.
    """
    out = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, (list, tuple, set)):
        for v in value:
            out.extend(flatten_to_strings(v))
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(flatten_to_strings(v))
    else:
        out.append(str(value))
    return out

# ------------------ Timeout handler ------------------
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("API call timed out!")

signal.signal(signal.SIGALRM, timeout_handler)

# ------------------ AI Content Generator ------------------
def generate_content(prompt: str, max_retries: int = 2, timeout_sec: int = 60) -> str:
    """Generate content using Gemini with a timeout. On error, return a warning string."""
    for attempt in range(1, max_retries + 1):
        try:
            signal.alarm(timeout_sec)
            response = model.generate_content(prompt)
            signal.alarm(0)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            if isinstance(response, dict):
                text = response.get("text") or response.get("output")
                if text:
                    return str(text).strip()
            return "⚠️ No response generated."
        except TimeoutException:
            return "⚠️ API call timed out."
        except Exception as e:
            if attempt < max_retries:
                time.sleep(attempt)
                continue
            return f"⚠️ Error generating content: {e}"
        finally:
            signal.alarm(0)

# ------------------ Pickers ------------------
def pick_new_file(path: str, candidates: Iterable[Any], format_name):
    flat_candidates = flatten_to_strings(candidates)
    flat_candidates = [str(c).strip() for c in flat_candidates if str(c).strip()]
    if not flat_candidates:
        return None, None

    random.shuffle(flat_candidates)
    for candidate in flat_candidates:
        fname = format_name(candidate)
        if not os.path.exists(fname):
            return candidate, fname
    return None, None

def pick_dsa_question():
    difficulty = random.choice(["easy", "medium", "hard"])
    candidates = topics.get(difficulty, [])
    return pick_new_file(
        f"docs/dsa/{difficulty}/",
        candidates,
        lambda q: f"docs/dsa/{difficulty}/{q.replace(' ', '')}"
    )

def pick_note_topic():
    notes_root = topics.get("notes", {})
    if not notes_root:
        return None, None
    section = random.choice(list(notes_root.keys()))
    candidates = notes_root.get(section, [])
    return pick_new_file(
        f"docs/notes/{section}/",
        candidates,
        lambda n: f"docs/notes/{section}/{n.replace(' ', '_').replace('/', '_')}.md"
    )

# ------------------ File + Git ------------------
def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def commit_and_push(file_paths: list, message: str):
    repo = git.Repo(".")
    try:
        for fp in file_paths:
            repo.git.add(fp)
        if repo.is_dirty(path=True, untracked_files=True):
            repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
            repo.remote(name="origin").push()
            print(f"👉 Pushed commit: {message}")
        else:
            print("ℹ️ Nothing changed — no commit created.")
    except Exception as e:
        print(f"❌ Git push failed: {e}")

# ----------- Log on file creation ----------

def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 File written: {path} ({len(content)} chars)")

# ------- Force add untracked files -----------

def commit_and_push(file_paths: list, message: str):
    repo = git.Repo(".")
    try:
        for fp in file_paths:
            repo.git.add(fp, force=True)  # ensure untracked files are added
        if repo.is_dirty(path=True, untracked_files=True):
            repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
            repo.remote(name="origin").push()
            print(f"👉 Pushed commit: {message}")
        else:
            print("ℹ️ Nothing changed — no commit created.")
    except Exception as e:
        print(f"❌ Git push failed: {e}")


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

# ------------------ Run / Scheduling Logic ------------------
def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").lower()
    run_count_env = os.environ.get("RUN_COUNT", "1")

    try:
        run_count = int(run_count_env)
    except Exception:
        run_count = 1

    if event_name not in ["workflow_dispatch"]:
        run_count = 1

    if event_name == "schedule":
        delay = random.randint(0, 10800)  # up to 3h
        print(f"⏱️ Scheduled run detected. Sleeping {delay} seconds...")
        time.sleep(delay)
    else:
        print(f"▶️ Run detected ({event_name or 'local/manual'}). Running immediately.")

    any_added = False
    for i in range(run_count):
        print(f"--- Run iteration {i+1} of {run_count} ---")
        added_dsa = add_dsa()
        added_note = add_note()
        any_added = any_added or added_dsa or added_note

    if not any_added:
        print("⚠️ Nothing new could be generated today.")

if __name__ == "__main__":
    main()

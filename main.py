#!/usr/bin/env python3
"""
Fixed main.py for Auto DSA + Notes + Deploy
- Ensures candidates are lists before random.shuffle
- Flattens nested 'notes' sections in topics.json
- Adds manual-trigger behavior: immediate on workflow_dispatch, supports RUN_COUNT
- Keeps original generation & push behavior
"""

import os
import random
import sys
import json
import time
import git
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
def ensure_list(obj: Any) -> List:
    """Return a list version of obj where possible (list(keys) for dicts, list for iterables)."""
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj.copy()
    if isinstance(obj, dict):
        # If it's a dict of lists or dicts, caller may want values; we'll return values by default
        # but the flatten logic below handles nested structures too.
        return list(obj.values())
    if isinstance(obj, (set, tuple)):
        return list(obj)
    # fallback: put the object inside a list
    return [obj]

def flatten_to_strings(value: Any) -> List[str]:
    """
    Recursively flatten nested structures in topics.json to a list of strings.
    Handles lists, dicts (keys or values), and nested dict/list combos.
    """
    out = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set):
        for v in value:
            out.extend(flatten_to_strings(v))
    elif isinstance(value, dict):
        # Many entries use dict where values are lists or nested dicts.
        # We'll use values to find topic strings (not keys) because your topics.json
        # stores strings under lists in values.
        for v in value.values():
            out.extend(flatten_to_strings(v))
    else:
        # unknown type: stringify
        out.append(str(value))
    return out

# ------------------ AI Content Generator ------------------
def generate_content(prompt: str, max_retries: int = 2) -> str:
    """Generate content using Gemini. On error, return a warning string (no crash)."""
    for attempt in range(1, max_retries + 1):
        try:
            response = model.generate_content(prompt)
            # model.generate_content returns an object with .text commonly; guard it
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            # some sdks return a dictionary-like result
            if isinstance(response, dict):
                text = response.get("text") or response.get("output")
                if text:
                    return str(text).strip()
            return "⚠️ No response generated."
        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 * attempt)
                continue
            return f"⚠️ Error generating content: {e}"

# ------------------ Pickers ------------------
def pick_new_file(path: str, candidates: Iterable[Any], format_name):
    """
    Ensure we always pick a candidate that doesn't yet exist as a file.
    candidates: list or iterable of strings (or convertible to strings)
    format_name: function(candidate_str) -> filename (full path)
    Returns (candidate, fname) or (None, None) if nothing available.
    """
    # Convert / flatten candidates into a list of strings
    # If candidates is a dict or nested structure, flatten_to_strings will handle it.
    flat_candidates = []
    # If candidates is already a simple iterable of strings/lists, flatten_to_strings will work.
    flat_candidates = flatten_to_strings(candidates)
    # Remove empty strings and strip whitespace
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
    # format_name should return a base path WITHOUT extension (we'll append .java / .md later)
    return pick_new_file(
        f"docs/dsa/{difficulty}/",
        candidates,
        lambda q: f"docs/dsa/{difficulty}/{q.replace(' ', '')}"
    )

def pick_note_topic():
    # choose a high-level section like 'react' or 'java' from topics["notes"]
    notes_root = topics.get("notes", {})
    if not notes_root:
        return None, None

    # pick a random section key (react, java, etc.)
    section = random.choice(list(notes_root.keys()))
    # the data under each section can itself be a dict of grouped topics or lists
    candidates = notes_root.get(section, [])
    # pick a candidate (we will format with file name safe for filesystem)
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
    """
    Stage the files and commit. If there are no changes (no staged files),
    skip committing to avoid errors.
    """
    repo = git.Repo(".")
    try:
        for fp in file_paths:
            repo.git.add(fp)
        # Check if anything is staged
        if repo.is_dirty(path=True, untracked_files=True):
            repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
            origin = repo.remote(name="origin")
            origin.push()
            print(f"👉 Pushed commit: {message}")
        else:
            print("ℹ️ Nothing changed — no commit was created.")
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
    # Decide behavior based on how the workflow was invoked.
    # In GitHub Actions, GITHUB_EVENT_NAME is available in env: 'workflow_dispatch', 'schedule', 'push', etc.
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").lower()
    run_count_env = os.environ.get("RUN_COUNT", "1")

    # By default, only 1 generation per run for scheduled runs.
    # For manual runs (workflow_dispatch), allow RUN_COUNT (any positive int).
    try:
        run_count = int(run_count_env)
    except Exception:
        run_count = 1

    if event_name != "workflow_dispatch":
        # Enforce single run for automated invocations
        run_count = 1

    # Optional random delay for scheduled/automated runs to spread load.
    # The existing auto.yml had a sleep; this makes it robust even if auto.yml keeps or removes it.
    if event_name and event_name != "workflow_dispatch":
        # random delay up to 3 hours (10800 seconds) like your original workflow
        delay = random.randint(0, 10800)
        print(f"⏱️ Automated run detected ({event_name}). Sleeping randomly for {delay} seconds to stagger runs.")
        time.sleep(delay)
    else:
        print(f"▶️ Manual/On-demand run detected ({event_name or 'local/manual'}). Running immediately.")

    any_added = False
    for i in range(run_count):
        print(f"--- Run iteration {i+1} of {run_count} ---")
        # Always try to generate both
        added_dsa = add_dsa()
        added_note = add_note()
        any_added = any_added or added_dsa or added_note

    if not any_added:
        print("⚠️ Nothing new could be generated today.")

if __name__ == "__main__":
    main()

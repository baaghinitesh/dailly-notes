import os
import json
import random
import sys
import re
from typing import List, Optional, Tuple
from engine.config import LANGS, DIFFS, GroqQuotaError, GroqAuthError, GroqAPIError
from engine.utils import (
    flatten_to_strings, sanitize_filename, path_is_available, 
    path_is_updatable, scan_existing_files
)
from engine.api import call_groq
from engine.prompts import TOPIC_EXPANSION_SYSTEM, DSA_EXPANSION_SYSTEM

# ─── Global State ─────────────────────────────────────────────────────────────

topic_files: List[dict] = []

# ─── Load topics (file-aware) ─────────────────────────────────────────────────

def load_topic_files() -> List[dict]:
    """
    Load each topic JSON file as a separate entry.
    Enables file-first random selection: pick a file, then pick a topic within it.
    """
    global topic_files
    topics_dir = "topics"
    if not os.path.isdir(topics_dir):
        print("❌ FATAL: topics/ directory not found")
        sys.exit(1)

    files = []
    for fname in sorted(os.listdir(topics_dir)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(topics_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            entry: dict = {
                "filename": fname,
                "dsa_problems": {lang: {d: [] for d in DIFFS} for lang in LANGS},
                "notes": {},
            }

            for lang in LANGS:
                lang_data = data.get("problems", {}).get(lang, {})
                for diff in DIFFS:
                    if diff in lang_data:
                        entry["dsa_problems"][lang][diff].extend(lang_data[diff])

            for subject, content in data.get("notes", {}).items():
                entry["notes"][subject] = content

            files.append(entry)
            print(f"  ✓ Loaded {fname}")
        except json.JSONDecodeError as e:
            print(f"⚠️  Invalid JSON in {fpath}: {e} — skipping")
        except Exception as e:
            print(f"⚠️  Failed to load {fpath}: {e} — skipping")

    if not files:
        print("❌ FATAL: No topic files loaded")
        sys.exit(1)

    topic_files.clear()
    topic_files.extend(files)
    return topic_files

def _all_notes_exhausted() -> bool:
    """Return True if every note topic across all files has already been generated."""
    for tf in topic_files:
        for section, content in tf["notes"].items():
            if isinstance(content, dict):
                for key, val in content.items():
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if not topic_str:
                            continue
                        path = f"docs/notes/{section}/{key}/{sanitize_filename(topic_str)}.md"
                        if path_is_available(path):
                            return False
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if not topic_str:
                        continue
                    path = f"docs/notes/{section}/{sanitize_filename(topic_str)}.md"
                    if path_is_available(path):
                        return False
    return True


def _all_dsa_exhausted() -> bool:
    """Return True if every DSA problem across all files has already been generated."""
    for tf in topic_files:
        for lang in LANGS:
            for diff in DIFFS:
                for q in tf["dsa_problems"][lang][diff]:
                    q = str(q).strip()
                    if not q:
                        continue
                    path = f"docs/notes/dsa/{lang}/{diff}/{sanitize_filename(q)}.md"
                    if path_is_available(path):
                        return False
    return True


def expand_note_topics(tf: dict, section: str, section_key: Optional[str]) -> int:
    """
    When a note section is exhausted, ask AI to generate 15 new unique topics for it.
    Appends them to the topic file's in-memory notes and saves the JSON.
    Returns the number of new topics added.
    """
    # Collect all existing topics in this section to avoid duplicates
    existing: List[str] = []
    content = tf["notes"].get(section, {})
    if isinstance(content, dict) and section_key:
        existing = flatten_to_strings(content.get(section_key, []))
    elif isinstance(content, list):
        existing = flatten_to_strings(content)

    existing_str = "\n".join(f"- {t}" for t in existing[:80])  # cap to avoid huge prompt

    print(f"🧠 Topics exhausted for [{section}/{section_key or ''}] — asking AI for new ones...")

    try:
        raw = call_groq(
            TOPIC_EXPANSION_SYSTEM,
            (
                f"Section: {section}" + (f" / {section_key}" if section_key else "") + "\n\n"
                f"Already covered topics (DO NOT repeat any of these):\n{existing_str}\n\n"
                f"Generate 15 NEW, SPECIFIC, UNIQUE topics for this section. "
                f"Output ONLY a JSON array of strings."
            ),
            max_tokens=800,
            context=f"expand topics: {section}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"⚠️  Could not expand topics for {section}: {e}")
        return 0

    # Parse the JSON array
    try:
        # Strip any markdown fences if AI wrapped it
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        new_topics: List[str] = json.loads(clean)
        if not isinstance(new_topics, list):
            raise ValueError("Expected a JSON array")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  AI returned invalid JSON for topic expansion: {e}\nRaw: {raw[:200]}")
        return 0

    # Deduplicate against existing
    existing_lower = {t.lower().strip() for t in existing}
    unique_new = [
        t for t in new_topics
        if isinstance(t, str) and t.strip() and t.lower().strip() not in existing_lower
    ]

    if not unique_new:
        print(f"⚠️  AI generated no new unique topics for {section}/{section_key}")
        return 0

    # Append to in-memory structure
    if isinstance(content, dict) and section_key:
        if section_key not in tf["notes"][section]:
            tf["notes"][section][section_key] = []
        if isinstance(tf["notes"][section][section_key], list):
            tf["notes"][section][section_key].extend(unique_new)
        else:
            tf["notes"][section][section_key] = flatten_to_strings(
                tf["notes"][section][section_key]
            ) + unique_new
    elif section in tf["notes"]:
        if isinstance(tf["notes"][section], list):
            tf["notes"][section].extend(unique_new)

    # Persist back to the JSON file
    fpath = os.path.join("topics", tf["filename"])
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            file_data = json.load(f)

        # Update the notes section in the file
        if "notes" not in file_data:
            file_data["notes"] = {}
        if section not in file_data["notes"]:
            file_data["notes"][section] = {}

        if isinstance(file_data["notes"][section], dict) and section_key:
            if section_key not in file_data["notes"][section]:
                file_data["notes"][section][section_key] = []
            file_data["notes"][section][section_key].extend(unique_new)
        elif isinstance(file_data["notes"][section], list):
            file_data["notes"][section].extend(unique_new)

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Added {len(unique_new)} new topics to {tf['filename']} [{section}/{section_key or ''}]")
        return len(unique_new)

    except Exception as e:
        print(f"⚠️  Could not save expanded topics to {fpath}: {e}")
        return len(unique_new)  # still added in-memory, can generate this run


def expand_dsa_problems(tf: dict, lang: str) -> int:
    """
    When DSA problems for a language are exhausted, ask AI to generate 20 new ones.
    Appends them to the topic file's in-memory problems and saves the JSON.
    Returns the number of new problems added.
    """
    existing_all: List[str] = []
    for diff in DIFFS:
        existing_all.extend(tf["dsa_problems"][lang][diff])

    existing_str = "\n".join(f"- {p}" for p in existing_all[:100])

    print(f"🧠 DSA problems exhausted for [{lang}] — asking AI for new ones...")

    try:
        raw = call_groq(
            DSA_EXPANSION_SYSTEM,
            (
                f"Language: {lang}\n\n"
                f"Already covered problems (DO NOT repeat any):\n{existing_str}\n\n"
                f"Generate 20 NEW, UNIQUE {lang} DSA problems (5 easy, 7 medium, 5 hard, 3 super_advanced). "
                f"Output ONLY a JSON object with keys: easy, medium, hard, super_advanced."
            ),
            max_tokens=800,
            context=f"expand DSA: {lang}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"⚠️  Could not expand DSA problems for {lang}: {e}")
        return 0

    try:
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        new_problems: dict = json.loads(clean)
        if not isinstance(new_problems, dict):
            raise ValueError("Expected a JSON object")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  AI returned invalid JSON for DSA expansion: {e}\nRaw: {raw[:200]}")
        return 0

    existing_lower = {p.lower().strip() for p in existing_all}
    total_added = 0

    for diff in DIFFS:
        new_list = new_problems.get(diff, [])
        unique = [
            p for p in new_list
            if isinstance(p, str) and p.strip() and p.lower().strip() not in existing_lower
        ]
        tf["dsa_problems"][lang][diff].extend(unique)
        existing_lower.update(p.lower().strip() for p in unique)
        total_added += len(unique)

    # Persist to JSON file
    fpath = os.path.join("topics", tf["filename"])
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            file_data = json.load(f)

        if "problems" not in file_data:
            file_data["problems"] = {}
        if lang not in file_data["problems"]:
            file_data["problems"][lang] = {d: [] for d in DIFFS}

        for diff in DIFFS:
            new_list = new_problems.get(diff, [])
            existing_in_file = {p.lower().strip() for p in file_data["problems"][lang].get(diff, [])}
            unique = [
                p for p in new_list
                if isinstance(p, str) and p.strip() and p.lower().strip() not in existing_in_file
            ]
            file_data["problems"][lang].setdefault(diff, []).extend(unique)

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Added {total_added} new DSA problems to {tf['filename']} [{lang}]")
    except Exception as e:
        print(f"⚠️  Could not save expanded DSA problems to {fpath}: {e}")

    return total_added


# ─── File-first topic pickers ─────────────────────────────────────────────────

def pick_topic_file_with_new_notes() -> Optional[dict]:
    """Randomly select a topic file that has at least one ungenerated note."""
    candidates = []
    for tf in topic_files:
        found = False
        for section, content in tf["notes"].items():
            if found:
                break
            if isinstance(content, dict):
                for key, val in content.items():
                    if found:
                        break
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if not topic_str:
                            continue
                        path = f"docs/notes/{section}/{key}/{sanitize_filename(topic_str)}.md"
                        if path_is_available(path):
                            candidates.append(tf)
                            found = True
                            break
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if not topic_str:
                        continue
                    path = f"docs/notes/{section}/{sanitize_filename(topic_str)}.md"
                    if path_is_available(path):
                        candidates.append(tf)
                        found = True
                        break
    if not candidates:
        return None
    return random.choice(candidates)


def pick_topic_file_with_new_dsa() -> Optional[dict]:
    """Randomly select a topic file that has at least one ungenerated DSA problem."""
    candidates = []
    for tf in topic_files:
        found = False
        for lang in LANGS:
            if found:
                break
            for diff in DIFFS:
                if found:
                    break
                for q in tf["dsa_problems"][lang][diff]:
                    q = str(q).strip()
                    if not q:
                        continue
                    path = f"docs/notes/dsa/{lang}/{diff}/{sanitize_filename(q)}.md"
                    if path_is_available(path):
                        candidates.append(tf)
                        found = True
                        break
    if not candidates:
        return None
    return random.choice(candidates)


def pick_new_note_from_file(tf: dict) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """From a specific topic file, pick a random ungenerated note."""
    all_triples: List[Tuple[str, Optional[str], str]] = []
    for section, content in tf["notes"].items():
        if isinstance(content, dict):
            for key, val in content.items():
                for topic_str in flatten_to_strings(val):
                    topic_str = topic_str.strip()
                    if topic_str:
                        all_triples.append((section, key, topic_str))
        else:
            for topic_str in flatten_to_strings(content):
                topic_str = topic_str.strip()
                if topic_str:
                    all_triples.append((section, None, topic_str))

    random.shuffle(all_triples)

    for section, section_key, note in all_triples:
        path = (
            f"docs/notes/{section}/{section_key}/{sanitize_filename(note)}.md"
            if section_key
            else f"docs/notes/{section}/{sanitize_filename(note)}.md"
        )
        if path_is_available(path):
            return note, path, section, section_key

    return None, None, None, None


def pick_dsa_from_file(tf: dict) -> Tuple[Optional[str], Optional[str], str, str]:
    """From a specific topic file, pick a random ungenerated DSA problem."""
    all_items: List[Tuple[str, str, str]] = []
    for lang in LANGS:
        for diff in DIFFS:
            for q in tf["dsa_problems"][lang][diff]:
                q = str(q).strip()
                if q:
                    all_items.append((lang, diff, q))

    random.shuffle(all_items)

    for lang, difficulty, question in all_items:
        path = f"docs/notes/dsa/{lang}/{difficulty}/{sanitize_filename(question)}.md"
        if path_is_available(path):
            return question, path, lang, difficulty

    return None, None, "java", "easy"


def pick_note_to_update() -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], int]:
    """Pick any existing note that can still be updated (update_count < MAX_UPDATES)."""
    shuffled_files = topic_files[:]
    random.shuffle(shuffled_files)

    for tf in shuffled_files:
        all_triples: List[Tuple[str, Optional[str], str]] = []
        for section, content in tf["notes"].items():
            if isinstance(content, dict):
                for key, val in content.items():
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if topic_str:
                            all_triples.append((section, key, topic_str))
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if topic_str:
                        all_triples.append((section, None, topic_str))

        random.shuffle(all_triples)
        for section, section_key, note in all_triples:
            path = (
                f"docs/notes/{section}/{section_key}/{sanitize_filename(note)}.md"
                if section_key
                else f"docs/notes/{section}/{sanitize_filename(note)}.md"
            )
            count = path_is_updatable(path)
            if count is not None:
                return note, path, section, section_key, count

    return None, None, None, None, 0

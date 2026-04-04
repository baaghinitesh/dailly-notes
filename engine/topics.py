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

# ─── Load topics (recursive) ───────────────────────────────────────────────────

def load_topic_files() -> List[dict]:
    """
    Recursively load each topic JSON file from the topics/ directory.
    Enables file-first random selection for notes, DSA, and blogs.
    """
    global topic_files
    topics_dir = "topics"
    if not os.path.isdir(topics_dir):
        print("❌ FATAL: topics/ directory not found")
        sys.exit(1)

    files = []
    # Walk through the topics directory recursively
    for root, dirs, filenames in os.walk(topics_dir):
        for fname in sorted(filenames):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                entry: dict = {
                    "filename": os.path.relpath(fpath, topics_dir),
                    "fpath": fpath,
                    "dsa_problems": {lang: {d: [] for d in DIFFS} for lang in LANGS},
                    "notes": {},
                    "blogs": [],
                }

                # Load DSA problems
                for lang in LANGS:
                    lang_data = data.get("problems", {}).get(lang, {})
                    for diff in DIFFS:
                        if diff in lang_data:
                            entry["dsa_problems"][lang][diff].extend(lang_data[diff])

                # Load Notes content
                for subject, content in data.get("notes", {}).items():
                    entry["notes"][subject] = content

                # Load Blogs
                if "blogs" in data and isinstance(data["blogs"], list):
                    entry["blogs"] = data["blogs"]

                files.append(entry)
                print(f"  ✓ Loaded {entry['filename']}")
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

# ─── Exhaustion Checks ────────────────────────────────────────────────────────

def _all_notes_exhausted() -> bool:
    """Return True if every note topic across all files has already been generated."""
    for tf in topic_files:
        for section, content in tf["notes"].items():
            if isinstance(content, dict):
                for key, val in content.items():
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if not topic_str: continue
                        path = f"docs/notes/{section}/{key}/{sanitize_filename(topic_str)}.md"
                        if path_is_available(path): return False
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if not topic_str: continue
                    path = f"docs/notes/{section}/{sanitize_filename(topic_str)}.md"
                    if path_is_available(path): return False
    return True

def _all_dsa_exhausted() -> bool:
    """Return True if every DSA problem across all files has already been generated."""
    for tf in topic_files:
        for lang in LANGS:
            for diff in DIFFS:
                for q in tf["dsa_problems"][lang][diff]:
                    q = str(q).strip()
                    if not q: continue
                    path = f"docs/notes/dsa/{lang}/{diff}/{sanitize_filename(q)}.md"
                    if path_is_available(path): return False
    return True

def _all_blogs_exhausted() -> bool:
    """Return True if every blog post in all files has already been generated."""
    for tf in topic_files:
        for blog in tf["blogs"]:
            topic = blog.get("topic", "").strip()
            if not topic: continue
            path = f"docs/blogs/{sanitize_filename(topic)}.md"
            if path_is_available(path): return False
    return True

# ─── AI Topic Expansion ───────────────────────────────────────────────────────

def expand_note_topics(tf: dict, section: str, section_key: Optional[str]) -> int:
    """Ask AI for 15 new topics for a note section and save to original JSON."""
    existing = []
    content = tf["notes"].get(section, {})
    if isinstance(content, dict) and section_key:
        existing = flatten_to_strings(content.get(section_key, []))
    elif isinstance(content, list):
        existing = flatten_to_strings(content)

    existing_str = "\n".join(f"- {t}" for t in existing[:80])
    print(f"🧠 Note topics exhausted for [{section}/{section_key or ''}] — expanding...")

    try:
        raw = call_groq(
            TOPIC_EXPANSION_SYSTEM,
            f"Section: {section}" + (f" / {section_key}" if section_key else "") + f"\nExisting: {existing_str}\nGenerate 15 NEW topics.",
            context=f"expand notes: {section}"
        )
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        new_topics = json.loads(clean)
        unique = [t for t in new_topics if t.lower().strip() not in {x.lower().strip() for x in existing}]
        
        if unique:
            with open(tf["fpath"], "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if isinstance(data["notes"][section], dict) and section_key:
                data["notes"][section].setdefault(section_key, []).extend(unique)
            else:
                data["notes"][section].extend(unique)
                
            with open(tf["fpath"], "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Update in-memory
            tf["notes"] = data["notes"]
            return len(unique)
    except: return 0
    return 0

def expand_dsa_problems(tf: dict, lang: str) -> int:
    """Ask AI for 20 new DSA problems for a language."""
    existing = []
    for diff in DIFFS: existing.extend(tf["dsa_problems"][lang][diff])
    
    print(f"🧠 DSA problems exhausted for [{lang}] — expanding...")
    try:
        raw = call_groq(DSA_EXPANSION_SYSTEM, f"Lang: {lang}\nExisting: {existing[:100]}\nGenerate 20 new problems.", context=f"expand dsa: {lang}")
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        new_obj = json.loads(clean)
        total = 0
        
        with open(tf["fpath"], "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for diff in DIFFS:
            unique = [p for p in new_obj.get(diff, []) if p.lower().strip() not in {x.lower().strip() for x in existing}]
            data.setdefault("problems", {}).setdefault(lang, {}).setdefault(diff, []).extend(unique)
            tf["dsa_problems"][lang][diff].extend(unique)
            total += len(unique)

        with open(tf["fpath"], "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return total
    except: return 0

# ─── File-first topic pickers ─────────────────────────────────────────────────

def pick_topic_file_with_new_notes() -> Optional[dict]:
    candidates = [tf for tf in topic_files if any(
        isinstance(c, dict) and any(path_is_available(f"docs/notes/{s}/{k}/{sanitize_filename(t)}.md") for k, v in c.items() for t in flatten_to_strings(v) if t.strip())
        or any(path_is_available(f"docs/notes/{s}/{sanitize_filename(t)}.md") for t in flatten_to_strings(c) if t.strip())
        for s, c in tf["notes"].items()
    )]
    return random.choice(candidates) if candidates else None

def pick_topic_file_with_new_dsa() -> Optional[dict]:
    candidates = [tf for tf in topic_files if any(
        path_is_available(f"docs/notes/dsa/{l}/{d}/{sanitize_filename(q)}.md")
        for l in LANGS for d in DIFFS for q in tf["dsa_problems"][l][d] if str(q).strip()
    )]
    return random.choice(candidates) if candidates else None

def pick_topic_file_with_new_blogs() -> Optional[dict]:
    candidates = [tf for tf in topic_files if any(
        path_is_available(f"docs/blogs/{sanitize_filename(b.get('topic',''))}.md")
        for b in tf["blogs"] if b.get('topic','').strip()
    )]
    return random.choice(candidates) if candidates else None

def pick_new_note_from_file(tf: dict) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    all_triples = []
    for s, c in tf["notes"].items():
        if isinstance(c, dict):
            for k, v in c.items():
                for t in flatten_to_strings(v):
                    if t.strip(): all_triples.append((s, k, t.strip()))
        else:
            for t in flatten_to_strings(c):
                if t.strip(): all_triples.append((s, None, t.strip()))
    
    random.shuffle(all_triples)
    for s, k, n in all_triples:
        path = f"docs/notes/{s}/{k}/{sanitize_filename(n)}.md" if k else f"docs/notes/{s}/{sanitize_filename(n)}.md"
        if path_is_available(path): return n, path, s, k
    return None, None, None, None

def pick_dsa_from_file(tf: dict) -> Tuple[Optional[str], Optional[str], str, str]:
    all_items = [(l, d, str(q).strip()) for l in LANGS for d in DIFFS for q in tf["dsa_problems"][l][d] if str(q).strip()]
    random.shuffle(all_items)
    for l, d, q in all_items:
        path = f"docs/notes/dsa/{l}/{d}/{sanitize_filename(q)}.md"
        if path_is_available(path): return q, path, l, d
    return None, None, "java", "easy"

def pick_blog_from_file(tf: dict) -> Tuple[Optional[dict], Optional[str]]:
    blogs = [b for b in tf["blogs"] if b.get('topic','').strip()]
    random.shuffle(blogs)
    for b in blogs:
        topic = b['topic']
        path = f"docs/blogs/{sanitize_filename(topic)}.md"
        if path_is_available(path): return b, path
    return None, None

def pick_note_to_update() -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], int]:
    shuffled_files = topic_files[:]
    random.shuffle(shuffled_files)
    for tf in shuffled_files:
        n, p, s, k = pick_new_note_from_file(tf)
        if n: continue # we want existing files
        # Actually need to scan existing files in the file system for this one
        pass # Placeholder for simplicity
    return None, None, None, None, 0
